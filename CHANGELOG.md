# Changelog

## Unreleased

## v0.1.1 – 2023-02-21

Some bug fixes and minor changes and improvements.

### Added

- auto name tool
- new values subpackage for special value input (FuIDs, ToolIDs, InputControl names etc)

### Fixed

- ~~ToolID Enums now convert to str at the appropriate time to avoid breaks~~

### Changed

- Actually, ToolID and other Enums are now SimpleNamespaces

## v0.1.0 – 2023-02-20

Ok, it's time to commit to a first release and try some semantic versioning from now on. Isn't this fun?
Here's what we got so far:

### Features

- Create compositions, tools and inputs statically and generate code to paste into Fusion
- Add tools into macros or groups and create instance inputs and outputs
- Publish and connect inputs
- Animate number inputs with a BezierSpline or position inputs with XYPath Modifier
- Intuitively assign values to inputs by using input = value notation...
- ...or add keyframes for animated inputs using input[frame] = value notation.
- Create Polylines from a list of point tuples (x, y)
- Add custom user controls to any tool
- And maybe some more that I forgot
