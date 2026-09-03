# Style Guidelines and Rules

## RPM Packaging Workflow

- **Do not modify or force-push changes to already tagged releases/builds**:
  When updating RPMs due to packaging issues or build failures, do not delete or modify existing git tags for failed releases. Instead, commit the fix, increment the Release number in the spec file, and tag the new version (e.g., bump from `0.9.44-1` to `0.9.44-2`). Only delete/overwrite tagged releases if there is an explicit and exceptional reason to do so.
