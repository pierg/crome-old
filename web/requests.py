from flask import request

from z3.src_z3.operations import *
from tests_old.component_selection_platooning import libraries
from web import socketio
from flask_socketio import emit
import json

from multiprocessing import Lock

from src_z3.parser import *

lock = Lock()

# SessionID -> Dict[name -> CGT]
sess_goals: [str, list] = {}

# SessionID -> root CGT
sess_cgts = {}


def get_goals(session_id):
    """Get a list goals of the session_id or create new entry and return an empty list"""

    with lock:
        if session_id in sess_goals.keys():
            return sess_goals[session_id]
        else:
            sess_goals[session_id] = {}
            return {}


def set_goals(session_id: str, goals_to_set: list):
    """Add the goals in list of goals of the session_id"""

    with lock:
        sess_goals[session_id] = goals_to_set


def get_cgt(session_id):
    """Get the CGT of the session_id or None"""

    with lock:
        if session_id in sess_cgts.keys():
            return sess_cgts[session_id]
        else:
            return None


def set_cgt(session_id: str, cgt: CGTGoal):
    """Set the CGT to session_id"""

    with lock:
        sess_cgts[session_id] = cgt


@socketio.on('cgt_example')
def cgt_example():
    print('-----------------------')
    print('Example request received from - %s' + request.sid)
    print('-----------------------')

    curpath = os.path.abspath(os.curdir)

    with open(os.path.join(curpath, 'web/static/data_examples/example_goals.json')) as json_file:
        goal_list = json.load(json_file)

    with open(os.path.join(curpath, 'web/static/data_examples/example_ops.json')) as json_file:
        operator_list = json.load(json_file)

    with open(os.path.join(curpath, 'web/static/data_examples/example_edges.json')) as json_file:
        edges_list = json.load(json_file)

    emit('goal_list', [json.dumps(goal_list),
                       json.dumps(operator_list),
                       json.dumps(edges_list)])

    # s_goals, s_cgt = platooning_example()
    #
    # set_goals(request.sid, s_goals)
    # set_cgt(request.sid, s_cgt)
    #
    # emit('notification',
    #      {'type': "success", 'content': "Example executed correctly"})
    #
    # render_goals(request.sid)


@socketio.on('goals_text')
def goals_text(message):
    print('-----------------------')
    print('Goals received from - %s' + request.sid)
    print('-----------------------')

    emit('notification',
         {'type': "success", 'content': "Goals received"})

    s_goals = get_goals(request.sid)

    n_goals = parse_from_string(message['data'])

    s_goals.update(n_goals)

    set_goals(request.sid, s_goals)

    emit('notification',
         {'type': "success", 'content': "Goals saved"})

    render_goals(request.sid)


@socketio.on('goals_link')
def goals_link(message):
    print('-----------------------')
    print('Goals link from - %s' + request.sid)
    print('-----------------------')

    # emit('notification',
    #      {'type': "success", 'content': "Linking goals received"})

    s_goals = get_goals(request.sid)
    s_cgt = get_cgt(request.sid)

    if message["operation"] == "composition":
        goals = message["goals"]
        comp_goals = []
        for g in goals:
            comp_goals.append(s_goals[g])

        try:
            new_goal = compose_goals(comp_goals, name=message["name"], description=message["description"])

        except Exception as e:
            txt = str(e)
            txt = "<br />".join(txt.split("\n"))
            emit('alert',
                 {'title': "Conflict detected", 'content': txt})
            return

        s_goals.update({message["name"]: new_goal})

        set_goals(request.sid, s_goals)

        emit('notification',
             {'type': "success", 'content': "New goal created"})

        render_goals(request.sid)

    elif message["operation"] == "conjunction":
        goals = message["goals"]
        conj_goals = []
        for g in goals:
            conj_goals.append(s_goals[g])

        try:
            new_goal = conjoin_goals(conj_goals, name=message["name"], description=message["description"])

        except Exception as e:
            txt = str(e)
            txt = "<br />".join(txt.split("\n"))
            emit('alert',
                 {'title': "Conflict detected", 'content': txt})
            return

        s_goals.update({message["name"]: new_goal})

        set_goals(request.sid, s_goals)

        emit('notification',
             {'type': "success", 'content': "New goal created"})

        render_goals(request.sid)


    elif message["operation"] == "refinement":
        abstract_goal_name = message["abstract"]
        refined_goal_name = message["refined"]

        abstract_goal = get_goals(request.sid)[abstract_goal_name]
        refined_goal = get_goals(request.sid)[refined_goal_name]

        try:
            refine_goal(abstract_goal, refined_goal)

        except Exception as e:
            txt = str(e)
            txt = "<br />".join(txt.split("\n"))
            emit('alert',
                 {'title': "Refinement unsuccessful", 'content': txt})
            return

        emit('alert',
             {'title': "Refinement successful", 'content': "Assumption propagated<br>Goals connected"})

        return


    elif message["operation"] == "mapping":
        goal_name_to_map = message["goal"]
        library_name = message["library"]

        s_goals = get_goals(request.sid)

        goal = s_goals[goal_name_to_map]

        library = libraries[library_name]

        try:
            new_goal, msg = mapping_complete(library, goal)

        except Exception as e:
            txt = str(e)
            txt = "<br />".join(txt.split("\n"))
            emit('alert',
                 {'title': "Mapping unsuccessful", 'content': txt})
            return

        abs_name = goal.get_name()
        ref_name = new_goal.get_name()
        s_goals.update({abs_name: goal})
        s_goals.update({ref_name: new_goal})

        print(goal)
        print(new_goal)

        set_goals(request.sid, s_goals)

        emit('notification',
             {'type': "success", 'content': "Goals added"})

        msg = "<br />".join(msg.split("\n"))
        emit('alert',
             {'title': "Mapping successful", 'content': msg})

        render_goals(request.sid)
        return


    else:
        raise Exception("Unknown operation")

    print(len(s_goals))

    set_goals(request.sid, s_goals)

    cgt_n_children = 0
    cgt_head = None
    for goal_name, goal in s_goals.items():
        n_children = goal.n_children()
        if n_children > cgt_n_children:
            cgt_n_children = n_children
            cgt_head = goal

    if cgt_head is not None:
        set_cgt(request.sid, cgt_head)
        print(cgt_head.get_name() + " SETTED")

    emit('notification',
         {'type': "success", 'content': "Goals saved"})

    render_goals(request.sid)


def navigate_dag(current_node, operator_list, edges_list):
    if current_node.sub_goals is not None and len(current_node.sub_goals) > 0:
        operator = current_node.sub_operation
        parent_node_name = current_node.get_name()
        op_node_name = parent_node_name + "_" + operator
        operator_list.append(
            {
                "id": op_node_name,
                "type": operator
            }
        )
        edges_list.append(
            {
                "source": parent_node_name,
                "target": op_node_name,
                "type": "refinement"
            }
        )

        for child in current_node.sub_goals:
            child_name = child.get_name()
            edges_list.append(
                {
                    "source": op_node_name,
                    "target": child_name,
                    "type": "input"
                }
            )
            navigate_dag(child, operator_list, edges_list)

    return


def render_goals(session_id):
    s_goals = get_goals(session_id)
    s_cgt = get_cgt(session_id)

    goal_list = []
    operator_list = []
    edges_list = []

    for name, cgtgoal in s_goals.items():
        desc = cgtgoal.get_description()
        contracts = cgtgoal.render_contracts()
        goal = {
            "name": name,
            "description": desc,
            "contract": contracts,
        }
        goal_list.append(goal)

    cgt_head = s_cgt

    if s_cgt is not None:
        navigate_dag(cgt_head, operator_list, edges_list)

    # curpath = os.path.abspath(os.curdir)
    # with open(os.path.join(curpath, "web/static/data_examples/new_goals.json"), 'w') as outfile:
    #     json.dump(goal_list, outfile)
    #
    # with open(os.path.join(curpath, "web/static/data_examples/new_ops.json"), 'w') as outfile:
    #     json.dump(operator_list, outfile)
    #
    # with open(os.path.join(curpath, "web/static/data_examples/new_edges.json"), 'w') as outfile:
    #     json.dump(edges_list, outfile)

    emit('goal_list', [json.dumps(goal_list),
                       json.dumps(operator_list),
                       json.dumps(edges_list)])
