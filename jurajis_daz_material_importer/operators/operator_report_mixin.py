from bpy.props import BoolProperty
from bpy.types import Operator


class OperatorReportMixin(Operator):
    message_prefix = "DAZ Material Import: "

    silent: BoolProperty(
        name="Silent",
        description="Do not report anything.",
    )

    def report_info(self, message: str):
        if not self.silent:
            self.report({"INFO"}, f"{self.message_prefix}{message}")

    def report_warning(self, message: str):
        if not self.silent:
            self.report({"WARNING"}, f"{self.message_prefix}{message}")

    def report_error(self, message: str):
        if not self.silent:
            self.report({"ERROR"}, f"{self.message_prefix}{message}")
