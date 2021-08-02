import os
from controller import Controller
from tools.storage import Store
from tools.strings import StringMng
from tools.strix import Strix

path = os.path.abspath(os.path.dirname(__file__))

spec_abstracted = "/specs/approximate_LTL_spec_abstracted"
spec_forced = "/specs/approximate_LTL_spec_abstracted"

abstracted_folder = f"{path}/results/LTL_abstracted"
forced_folder = f"{path}/results/LTL_forced"


def evaluate(spec: str, result_folder: str):
    print(f"controller selected: {path}/{spec}.txt")

    a, g, i, o = StringMng.parse_controller_specification_from_file(f"{path}/{spec}.txt")
    realizable, kiss_format, exec_time = Strix.generate_controller(a, g, i, o)

    controller = Controller(mealy_machine=kiss_format, synth_time=exec_time)

    res = f"TIME MONOLITHIC SYNTHESIS    \t= {exec_time}\nN OF STATES:\t{len(controller.states)}\nN OF EDGES:\t{len(controller.transitions)}"

    print("\n~~~MEALY MACHINE~~~\n" + str(controller))

    run = controller.simulate_day_night()
    print("\n\n\n~~~SIMULATION OF A RUN~~~\n" + run)

    Store.save_to_file(res, f"results.txt", absolute_folder_path=result_folder)
    Store.save_to_file(str(run), f"run.txt", absolute_folder_path=result_folder)

    print(f"\n\nRESULTS:\n{res}")


if __name__ == '__main__':
    evaluate(spec_abstracted, abstracted_folder)
    evaluate(spec_forced, forced_folder)
