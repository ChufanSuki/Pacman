# loading dcop
dcop = load_dcop_from_file(dcop_files)
# build computation graph
cg = graph_module.build_computation_graph(dcop)
# Distributing computation graph
distribution = dist_module.distribute(
    cg,
    dcop.agents.values(),
    hints=dcop.dist_hints,
    computation_memory=algo_module.computation_memory,
    communication_load=algo_module.communication_load,
)
# Build AlgorithmDef
algo = build_algo_def(algo_module, args.algo, dcop.objective, args.algo_params)
# Create orchestrator
agents = dcop.agents
comm = InProcessCommunicationLayer()
orchestrator = Orchestrator(algo, cg, distribution, comm, dcop, infinity)
orchestrator.start()
# Create and start all agents.
# Each agent will register it-self on the orchestrator
for a_name in dcop.agents:
    comm = InProcessCommunicationLayer()
    agent = OrchestratedAgent(agents[a_name], comm,
                              orchestrator.address)
    agent.start()

orchestrator.deploy_computations()
orchestrator.run(timeout=timeout)

self._own_agt.start()
self._own_agt.run(self.directory.directory_computation.name)

self._own_agt.add_computation(self.mgt, ORCHESTRATOR_MGT)
self._own_agt.run(self.mgt.name)

self._computations[self.discovery.discovery_computation.name] = \
    self.discovery.discovery_computation
self.discovery.register_computation(
    self.discovery.discovery_computation.name,
    self.name, self.address)
elf.discovery.register_agent(self.name, self.address)
self.discovery.discovery_computation.start()

agt_dir = Agent('agt_dir',InProcessCommunicationLayer())
agt_dir.start()
directory = Directory(agt_dir.discovery)
agt_dir.add_computation(directory.directory_computation)
agt_dir.discovery.use_directory('agt_dir', agt_dir.address)
agt_dir.run(directory.directory_computation.name)

agt_dis = Agent('agt_dis', comm)
agt_dis.discovery.use_directory('agt_dir', agt_dir.address)
agt_dis.start()

def on_new_cycle(self, messages, cycle_id):

    # Collect costs messages from neighbor factors for this cycle (aka iteration)
    for sender, (message, t) in messages.items():
        self.costs[sender] = message.costs

    # select our value, based on new costs
    self.value_selection(*select_value(self.variable, self.costs, self.mode))

    # Compute and send our own costs to  factors.

    for f_name in self.factors:
        costs_f = costs_for_factor(self.variable, f_name, self.factors, self.costs)
        prev_costs, count = self._prev_messages[f_name]

        # Apply damping to computed costs:
        if self.damping_nodes in ["vars", "both"]:
            costs_f = apply_damping(costs_f, prev_costs, self.damping)

        # Check if there was enough change to send the message
        if not approx_match(costs_f, prev_costs, self.stability_coef):
            # Not same as previous : send
            self.post_msg(f_name, MaxSumMessage(costs_f))
            self._prev_messages[f_name] = costs_f, 1

        elif count < SAME_COUNT:
            # Same as previous, but not yet sent SAME_COUNT times: send
            self.post_msg(f_name, MaxSumMessage(costs_f))
            self._prev_messages[f_name] = costs_f, count + 1
        else:
            # Same and already sent SAME_COUNT times: no-send
            pass
    return None


def on_new_cycle(self, messages, cycle_id) -> Optional[List]:

    # Collect costs messages from neighbor variables for this cycle (aka iteration)
    for sender, (message, t) in messages.items():
        self._costs[sender] = message.costs

    for v in self.variables:
        costs_v = factor_costs_for_var(self.factor, v, self._costs, self.mode)
        prev_costs, count = self._prev_messages[v.name]

        # Apply damping to computed costs:
        if self.damping_nodes in ["factors", "both"]:
            costs_v = apply_damping(
                costs_v, prev_costs, self.damping
            )

        # Check if there was enough change to send the message
        if not approx_match(
                costs_v, prev_costs, self.stability_coef
        ):
            # Not same as previous : send
            self.post_msg(v.name, MaxSumMessage(costs_v))
            self._prev_messages[v.name] = costs_v, 1

        elif count < SAME_COUNT:
            # Same as previous, but not yet sent SAME_COUNT times: send
            self.post_msg(v.name, MaxSumMessage(costs_v))
            self._prev_messages[v.name] = costs_v, count + 1
        else:
            # Same and already sent SAME_COUNT times: no-send
            pass

    return None