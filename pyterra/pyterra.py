import subprocess
import os

class TerraformWrapper:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def _run_command(self, command):
        try:
            result = subprocess.run(
                command,
                cwd=self.working_dir,
                text=True,
                capture_output=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command '{' '.join(command)}' failed: {e.stderr}")

    def init(self):
        """Initialize the Terraform working directory."""
        return self._run_command(["terraform", "init"])

    def plan(self, out_file=None):
        """Generate and show an execution plan."""
        command = ["terraform", "plan"]
        if out_file:
            command.extend(["-out", out_file])
        return self._run_command(command)

    def apply(self, plan_file=None):
        """Apply the changes required to reach the desired state."""
        command = ["terraform", "apply"]
        if plan_file:
            command.append(plan_file)
        else:
            command.append("-auto-approve")
        return self._run_command(command)

    def destroy(self):
        """Destroy the Terraform-managed infrastructure."""
        return self._run_command(["terraform", "destroy", "-auto-approve"])

    def output(self, name=None):
        """Get the value of an output variable."""
        command = ["terraform", "output"]
        if name:
            command.append(name)
        return self._run_command(command)
    
    def workspace_list(self):
        """List all Terraform workspaces."""
        return self._run_command(["terraform", "workspace", "list"])

    def workspace_show(self):
        """Show the current Terraform workspace."""
        return self._run_command(["terraform", "workspace", "show"])

    def workspace_new(self, name):
        """Create a new Terraform workspace."""
        return self._run_command(["terraform", "workspace", "new", name])

    def workspace_select(self, name):
        """Select a Terraform workspace."""
        return self._run_command(["terraform", "workspace", "select", name])

    def workspace_delete(self, name):
        """Delete a Terraform workspace."""
        return self._run_command(["terraform", "workspace", "delete", name])