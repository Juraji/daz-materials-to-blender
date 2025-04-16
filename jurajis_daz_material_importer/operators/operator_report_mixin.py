from bpy.types import Operator


class OperatorReportMixin(Operator):
    def report_info(self, message: str):
        self.report({"INFO"}, f"DAZ Material Import: {message}")

    def report_warning(self, message: str):
        self.report({"WARNING"}, f"DAZ Material Import: {message}")

    def report_error(self, message: str):
        self.report({"ERROR"}, f"DAZ Material Import: {message}")
