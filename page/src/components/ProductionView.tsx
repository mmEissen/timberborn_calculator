import { useContext } from "react"
import { Graphviz } from 'graphviz-react';
import { TimberbornContext } from "../pyodideContext";
import ReactFlow, {
    addEdge,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
} from "reactflow"

import 'reactflow/dist/style.css';

interface Params {
    faction: string | null;
    product: string | null;
}


export function ProductionView(params: Params) {
    const timberborn = useContext(TimberbornContext);

    if (
        params.faction === null
        || params.product === null
    ) {
        return <></>
    }

    const [nodes, edges] = timberborn.graph(params.faction, params.product);

    console.log(nodes, edges)

    const nodes1 = [
        {
            id: '2',
            data: {
            label: 'Default Node',
            },
            position: { x: 100, y: 100 },
        }
    ]

    // return <Graphviz dot={dot}></Graphviz>
    return <ReactFlow
        nodes={nodes1}
        fitView
    >
        <Controls />
        <Background color="#aaa" gap={16} />
    </ReactFlow>
}