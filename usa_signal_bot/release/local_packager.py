import shutil
import zipfile
from pathlib import Path
from typing import List, Optional
import datetime
from usa_signal_bot.release.release_models import (
    ReleaseBuildRequest, ReleaseBuildResult, ReleaseManifest, ReleaseArtifact,
    create_release_build_id, validate_release_build_request, OperatorRunbook
)
from usa_signal_bot.core.enums import ReleaseStatus, ReleaseValidationStatus, ReleaseArtifactType
from usa_signal_bot.release.versioning import build_release_version
from usa_signal_bot.release.artifact_collector import collect_release_artifacts
from usa_signal_bot.release.release_manifest import build_release_manifest, write_release_manifest_json, write_release_manifest_markdown
from usa_signal_bot.release.changelog import generate_changelog_from_docs, write_changelog_markdown
from usa_signal_bot.release.runbook_generator import generate_operator_runbook, write_runbook_markdown

class LocalReleasePackager:
    def __init__(self, project_root: Path, data_root: Optional[Path] = None):
        self.project_root = project_root
        self.data_root = data_root if data_root else project_root / "data"

    def build(self, request: ReleaseBuildRequest) -> ReleaseBuildResult:
        try:
            validate_release_build_request(request)
        except Exception as e:
            return ReleaseBuildResult(
                build_id=create_release_build_id(),
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                status=ReleaseStatus.FAILED,
                request=request,
                manifest=None,
                bundle_path=None,
                validation_status=ReleaseValidationStatus.FAILED,
                errors=[f"Validation error: {e}"]
            )

        build_id = create_release_build_id()
        staging_dir = self.data_root / "release" / "staging" / build_id
        bundle_dir = self.data_root / "release" / "builds" / build_id

        try:
            staging_dir.mkdir(parents=True, exist_ok=True)
            bundle_dir.mkdir(parents=True, exist_ok=True)

            # 1. Versioning
            version = build_release_version(project_root=self.project_root)

            # 2. Artifact Collection
            collection = collect_release_artifacts(self.project_root, request)

            # 3. Stage artifacts
            staged_artifacts = self.stage_artifacts(staging_dir, collection.artifacts)

            # 4. Runbook
            runbook = generate_operator_runbook(self.project_root)

            # 5. Changelog
            entries = generate_changelog_from_docs(self.project_root)

            # 6. Manifest
            manifest = build_release_manifest(request.release_name, version, staged_artifacts)

            # 7. Write extra files to staging
            self.write_release_files(staging_dir, manifest, runbook, entries)

            # Add them to manifest
            from usa_signal_bot.release.release_manifest import build_release_artifact
            staged_artifacts.append(build_release_artifact(staging_dir / "RELEASE_MANIFEST.json", "RELEASE_MANIFEST.json", ReleaseArtifactType.MANIFEST))
            staged_artifacts.append(build_release_artifact(staging_dir / "RELEASE_MANIFEST.md", "RELEASE_MANIFEST.md", ReleaseArtifactType.MANIFEST))
            staged_artifacts.append(build_release_artifact(staging_dir / "OPERATOR_RUNBOOK.md", "OPERATOR_RUNBOOK.md", ReleaseArtifactType.RUNBOOK))
            staged_artifacts.append(build_release_artifact(staging_dir / "CHANGELOG.md", "CHANGELOG.md", ReleaseArtifactType.CHANGELOG))
            manifest = build_release_manifest(request.release_name, version, staged_artifacts)

            # 8. Create Zip Bundle
            output_path = bundle_dir / f"{request.release_name}.zip"
            self.create_zip_bundle(staging_dir, output_path)

            # 9. Validate bundle
            val_status = ReleaseValidationStatus.PASSED
            if request.validate_after_build:
                val_status = self.validate_bundle(output_path, manifest)

            # 10. Cleanup
            self.clean_staging_dir(staging_dir)

            return ReleaseBuildResult(
                build_id=build_id,
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                status=ReleaseStatus.BUILT,
                request=request,
                manifest=manifest,
                bundle_path=str(output_path),
                validation_status=val_status,
                output_paths={"bundle": str(output_path)}
            )

        except Exception as e:
            self.clean_staging_dir(staging_dir)
            return ReleaseBuildResult(
                build_id=build_id,
                created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                status=ReleaseStatus.FAILED,
                request=request,
                manifest=None,
                bundle_path=None,
                validation_status=ReleaseValidationStatus.FAILED,
                errors=[str(e)]
            )

    def stage_artifacts(self, staging_dir: Path, artifacts: List[ReleaseArtifact]) -> List[ReleaseArtifact]:
        staged = []
        for artifact in artifacts:
            if not artifact.included:
                continue
            src = Path(artifact.source_path)
            if src.exists() and src.is_file():
                tgt = staging_dir / artifact.target_path
                tgt.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, tgt)
                staged.append(artifact)
        return staged

    def create_zip_bundle(self, staging_dir: Path, output_path: Path) -> Path:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in staging_dir.walk():
                for file in files:
                    file_path = root / file
                    arcname = file_path.relative_to(staging_dir)
                    zipf.write(file_path, arcname)
        return output_path

    def write_release_files(self, staging_dir: Path, manifest: ReleaseManifest, runbook: Optional[OperatorRunbook] = None, changelog_entries: list = None) -> dict:
        paths = {}
        paths['manifest_json'] = str(write_release_manifest_json(staging_dir / "RELEASE_MANIFEST.json", manifest))
        paths['manifest_md'] = str(write_release_manifest_markdown(staging_dir / "RELEASE_MANIFEST.md", manifest))
        if runbook:
            paths['runbook'] = str(write_runbook_markdown(staging_dir / "OPERATOR_RUNBOOK.md", runbook))
        if changelog_entries:
            paths['changelog'] = str(write_changelog_markdown(staging_dir / "CHANGELOG.md", changelog_entries))
        return paths

    def validate_bundle(self, bundle_path: Path, manifest: ReleaseManifest) -> ReleaseValidationStatus:
        if not bundle_path.exists():
            return ReleaseValidationStatus.FAILED
        try:
            with zipfile.ZipFile(bundle_path, 'r') as zipf:
                files = zipf.namelist()
                if "RELEASE_MANIFEST.json" not in files:
                    return ReleaseValidationStatus.FAILED
                for artifact in manifest.artifacts:
                    # Windows paths in target_path might have backward slashes, Zip uses forward
                    expected = artifact.target_path.replace("\\", "/")
                    if expected not in files:
                        return ReleaseValidationStatus.WARNING
            return ReleaseValidationStatus.PASSED
        except Exception:
            return ReleaseValidationStatus.FAILED

    def clean_staging_dir(self, staging_dir: Path) -> None:
        if staging_dir.exists():
            shutil.rmtree(staging_dir, ignore_errors=True)
