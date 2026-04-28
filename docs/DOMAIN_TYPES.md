# Domain Types and Enums

This project relies on centralized enums and types to ensure consistency across all modules without causing circular dependencies.

## Enums (`core/enums.py`)
Centralized enums provide strict categorization for key domain concepts:

- `AssetType`: Defines whether an asset is a `STOCK` or `ETF`.
- `TimeFrame`: Standardized bar intervals (`ONE_MINUTE`, `ONE_DAY`, etc.).
- `SignalSide` / `PositionSide`: Represents directionality (`LONG`, `SHORT`, `FLAT`).
- `OrderStatus`: Tracks the lifecycle of a simulated order (`CREATED`, `FILLED`, `REJECTED`, etc.).
- `RegimeType`: Broad market environment categories.

*All enums are string-based (`str, Enum`) to simplify JSON serialization.*

## Type Aliases (`core/types.py`)
Type aliases clarify intent in function signatures and dataclasses:
- `Symbol`, `Currency`, `TimeFrameValue`
- `Numeric`, `JsonDict`, `JsonList`

## Validation Standard (`core/model_validation.py`)
Centralized validation functions ensure data integrity when models are instantiated. Functions like `ensure_positive_number` and `ensure_ratio` raise a custom `DataValidationError` if criteria aren't met.

## Serialization Standard (`core/serialization.py`)
All models can be safely converted to dictionaries and JSON strings via utility functions that natively handle `Enum`, `Path`, nested `dataclasses`, and lists/dicts of these types.
