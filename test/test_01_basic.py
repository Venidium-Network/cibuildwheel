import os
import textwrap
from . import utils


def test(tmpdir):
    project_dir = str(tmpdir)

    utils.generate_project(
        path=project_dir,
        setup_py_add=textwrap.dedent('''
            import os
                            
            if os.environ.get("CIBUILDWHEEL", "0") != "1":
                raise Exception("CIBUILDWHEEL environment variable is not set to 1")
        ''')
    )

    # build the wheels
    actual_wheels = utils.cibuildwheel_run(project_dir)

    # check that the expected wheels are produced
    expected_wheels = utils.expected_wheels("spam", "0.1.0")
    assert set(actual_wheels) == set(expected_wheels)


def test_build_identifiers(tmpdir):
    project_dir = str(tmpdir)

    utils.generate_project(
        path=project_dir,
    )

    # check that the number of expected wheels matches the number of build
    # identifiers
    # after adding CIBW_MANYLINUX_IMAGE to support manylinux2010, there
    # can be multiple wheels for each wheel, though, so we need to limit
    # the expected wheels
    expected_wheels = [
        w
        for w in utils.expected_wheels("spam", "0.1.0")
        if not "-manylinux" in w or "-manylinux1" in w
    ]
    build_identifiers = utils.cibuildwheel_get_build_identifiers(project_dir)
    assert len(expected_wheels) == len(build_identifiers)
