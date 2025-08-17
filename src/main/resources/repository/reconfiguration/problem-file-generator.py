def generate_problem_file(num_components, target_instances,init_instances, output_file="scale-up.pddl"):
    components = [f"c{i}" for i in range(num_components)]
    ports = [f"p{i}" for i in range(num_components)]

    objects = "    s0 - space\n"
    objects += "    " + " ".join(components) + " - component\n"
    objects += "    " + " ".join(ports) + " - port\n"

    init = [
        "    (= (instance-number) 0)",
        "    (= (next-instance-id) 0)"
    ]

    for c in components:
        init.append(f"    (= (component-instance-number {c}) {init_instances})")
        init.append(f"    (= (component-should-have-instance-number {c}) {target_instances})")

    for i, c in enumerate(components):
        init.append(f"    (running-provide {c} {ports[i]})")

    for i in range(1, num_components):
        init.append(f"    (running-require {components[i]} {ports[i-1]})")

    goal_tasks = "\n      ".join([f"(scaleUp {c})" for c in components])

    problem = f"""(define (problem scale-up-example)
  (:domain reconfiguration)
  (:requirements :strips :fluents)
  (:objects
{objects}  )
  (:init
{chr(10).join(init)}
  )
  (:goal-tasks
    (sequence
      {goal_tasks}
    )
  )
)
"""
    with open(output_file, "w") as f:
        f.write(problem)

    print(f"✅ Problem file generated: {output_file}")


if __name__ == "__main__":
    generate_problem_file(num_components=4, init_instances=1, target_instances=5)
