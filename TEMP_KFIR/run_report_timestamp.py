import os
import pytest
from datetime import datetime


def set_up_reports():
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = 'Reports'
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"{report_dir}/report_{timestamp}.html"

    # Run pytest and generate report
    pytest.main([f"--html={report_filename}", "--self-contained-html"])


if __name__ == "__main__":
    set_up_reports()
