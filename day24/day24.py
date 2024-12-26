# https://adventofcode.com/2024/day/24

from dataclasses import dataclass


@dataclass(frozen=True)
class Gate:
    type: str
    output: str
    inputs: frozenset

    def execute(self, input1, input2):
        if self.type == "AND":
            return input1 and input2
        elif self.type == "OR":
            return input1 or input2
        elif self.type == "XOR":
            return input1 != input2
        raise ValueError(f"Invalid gate type {self.type}")

    def __repr__(self):
        inputs = list(self.inputs)
        return f"{inputs[0]} {self.type} {inputs[1]} -> {self.output}"


def q1(lines):
    wires = {
        w[0]: w[1].strip() == "1" for w in [l.split(":") for l in lines if ":" in l]
    }
    gates = {
        Gate(g[1], g[4], frozenset({g[0], g[2]}))
        for g in [l.split() for l in lines if "->" in l]
    }

    return run(wires, gates)


def run(wires, gates):
    events = list(wires.keys())
    while events:
        event = events.pop(0)
        for gate in gates:
            if event in gate.inputs:
                if all(i in wires for i in gate.inputs):
                    inputs = iter(gate.inputs)
                    wires[gate.output] = gate.execute(
                        wires[next(inputs)], wires[next(inputs)]
                    )
                    events.append(gate.output)
    return int(
        "".join(
            list(
                map(
                    lambda k: "1" if wires[k] else "0",
                    sorted([k for k in wires.keys() if k[0] == "z"], reverse=True),
                )
            )
        ),
        2,
    )


def q2(lines):
    gates = {
        Gate(g[1], g[4], frozenset({g[0], g[2]}))
        for g in [l.split() for l in lines if "->" in l]
    }
    # return generate_dot_code(gates)

    bits = max(int(l.split(":")[0][1:]) for l in lines if ":" in l)
    for bit in range(bits):
        # test each bit: 0+0, 0+1, 1+0, 1+1, and repeat with one carried
        for carry in [0, 1]:
            for a in [0, 1]:
                for b in [0, 1]:
                    wires = {f"x{bit:02}": a == 1, f"y{bit:02}": b == 1}
                    if carry:
                        if bit == 0:
                            continue
                        wires |= {f"x{bit-1:02}": True, f"y{bit-1:02}:": True}

                    wires_snapshot = wires.copy()
                    for i in range(bits):
                        _ = wires.setdefault(f"x{i:02}", False)
                        _ = wires.setdefault(f"y{i:02}", False)

                    output = run(wires, gates)

                    expected = (a + b) << bit
                    if carry:
                        expected += 1 << (bit - 1)

                    if output != +expected:
                        print(
                            f"Bit {bit} failed: {a}, {b}, {carry} -> {output} ({expected=}) # {wires_snapshot}"
                        )
                        # print(bin(output))
                        # print(bin(expected))


# 1: hmk/z16
# WAS: vmr XOR bnc -> hmk, y16 AND x16 -> z16
# NOW: vmr XOR bnc -> z16, y16 AND x16 -> hmk

# 2: fhp/z20
# WAS: tsc XOR pns -> fhp, pns AND tsc -> z20
# NOW: tsc XOR pns -> z20, pns AND tsc -> fhp

# 3: rvf/tpc
# WAS: x27 AND y27 -> rvf, y27 XOR x27 -> tpc
# NOW: x27 AND y27 -> tpc, y27 XOR x27 -> rvf

# 4: z33/fcd
# WAS:
# NOW:


def generate_dot_code(gates):
    dot_code = "digraph InputsToOutputs {\n"
    dot_code += "    node[shape=box];\n"

    nodes = set()
    edges = []

    for gate in gates:
        for input_node in gate.inputs:
            if input_node not in nodes:
                nodes.add(input_node)
                dot_code += f'    {input_node}[label="{input_node}"];\n'

        if gate.output not in nodes:
            nodes.add(gate.output)
            dot_code += f'    {gate.output}[label="{gate.output}"];\n'

        for input_node in gate.inputs:
            edges.append((input_node, gate.output, gate.type))

    for edge in edges:
        input_node, output_node, operator = edge
        color = "green" if operator == "AND" else "red" if operator == "OR" else "blue"
        dot_code += (
            f'    {input_node} -> {output_node}[label="{operator}", color={color}];\n'
        )

    dot_code += "}\n"
    return dot_code
