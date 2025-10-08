from hardware_interaction import coap
from utils import KLogger

log = KLogger(__name__)


def get_status(subsystem):
    result = coap.run_script('regread32 0xffff1c10080', subsystem, expect_return=True)
    if result is None:
        result = 0
    status = int(result, 0)
    speed = (status & 0xF0000) >> 16
    width = (status & 0x3F00000) >> 20

    log.info("{}: PCIe East West link speed is Gen{}".format(subsystem.name, speed))
    log.info("{}: PCIe East West link width is x{}".format(subsystem.name, width))

    return speed, width


def check_status(subsystem, speed, width):
    if speed != 0x4:
        subsystem.fail("PCIe East-West link speed is Gen{} not Gen4".format(speed))
    if width != 0x4:
        subsystem.fail("PCIe East-West link width is x{} not x4".format(width))


def check_ew_link_status(tester, progress_bar):
    for subsystem in tester.valid_subsystems():
        progress_bar.render_progress()
        try:
            speed, width = get_status(subsystem)
        except ValueError as ex:
            log.exception(ex, "{}: Value error when parsing results of COAP regread".format(subsystem.name))
            subsystem.fail("PCIe East-West Link Status: Invalid COAP response")
        else:
            check_status(subsystem, speed, width)



