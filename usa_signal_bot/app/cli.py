import click
from pathlib import Path
from usa_signal_bot.feature_engine.core_indicators.indicator_implementation_registry import indicator_implementation_registry_to_text, build_core_indicator_computation_specs
from usa_signal_bot.feature_engine.core_indicators.feature_table_builder import build_core_feature_table_from_csv
from usa_signal_bot.feature_engine.core_indicators.core_indicator_store import write_feature_table_csv
from usa_signal_bot.feature_engine.core_indicators.core_indicator_report import build_core_indicator_full_review, core_indicator_full_review_to_text

@click.group()
def cli():
    pass

@cli.command()
def core_indicators_info():
    click.echo("Phase 117 Core Indicators")
    click.echo("NOTE: Phase 117 is NOT activation. Indicator/feature outputs are NOT trade signals.")

@cli.command()
def indicator_implementation_registry():
    specs = build_core_indicator_computation_specs()
    click.echo(indicator_implementation_registry_to_text(specs))

@cli.command()
@click.option('--input', type=click.Path(exists=True), required=True)
@click.option('--write', is_flag=True, help="Write output to disk")
def build_core_feature_table(input, write):
    df, res = build_core_feature_table_from_csv(Path(input))
    if write:
        out_path = Path("data/feature_engine/core_indicators/feature_tables/output.csv")
        write_feature_table_csv(out_path, df, overwrite=True)
        click.echo(f"Table written to {out_path}")
    else:
        click.echo(f"Feature table preview: {res.rows} rows, {len(res.feature_columns)} feature columns")
        click.echo(f"Valid schema: {res.schema.schema_valid}")

@cli.command()
@click.option('--write', is_flag=True)
def core_indicator_review(write):
    rev = build_core_indicator_full_review()
    click.echo(core_indicator_full_review_to_text(rev))

if __name__ == '__main__':
    cli()
