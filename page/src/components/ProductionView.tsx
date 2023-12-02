import { useContext } from "react"
import { TimberbornContext } from "../pyodideContext";
import ReactFlow, {
    Controls,
    Background,
} from "reactflow"
import dagre from 'dagre';

import 'reactflow/dist/style.css';
import { ProductionNode } from "./ProductionNode";

interface Params {
    faction: string | null;
    product: string | null;
}

const nodeTypes = {
    productionNode: ProductionNode
}

// Copy pasta from https://reactflow.dev/examples/layout/dagre
const getLayoutedElements = (nodes: any, edges: any, direction = 'TB') => {
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));

    const nodeWidth = 256;
    const nodeHeight = 128;

    const isHorizontal = direction === 'LR';
    dagreGraph.setGraph({ rankdir: direction });

    nodes.forEach((node: any) => {
        dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });

    edges.forEach((edge: any) => {
        dagreGraph.setEdge(edge.source, edge.target);
    });

    dagre.layout(dagreGraph);

    nodes.forEach((node: any) => {
        const nodeWithPosition = dagreGraph.node(node.id);
        node.targetPosition = isHorizontal ? 'left' : 'top';
        node.sourcePosition = isHorizontal ? 'right' : 'bottom';

        // We are shifting the dagre node position (anchor=center center) to the top left
        // so it matches the React Flow node anchor point (top left).
        node.position = {
            x: nodeWithPosition.x - nodeWidth / 2,
            y: nodeWithPosition.y - nodeHeight / 2,
        };

        return node;
    });

    return { nodes, edges };
};

export function ProductionView(params: Params) {
    const timberborn = useContext(TimberbornContext);

    if (
        params.faction === null
        || params.product === null
    ) {
        return <></>
    }

    const [timberNodes, timberEdges] = timberborn.graph(params.faction, params.product);

    const nodes = timberNodes.map(timberNode => {
        return {
            id: timberNode.id,
            type: "productionNode",
            data: {
                facilityName: timberNode.facilityName,
                recipeName: timberNode.recipeName,
                resources: timberNode.resourceNames,
                products: timberNode.productNames,
                numberFacilities: timberNode.numberFacilities
            },
        }
    });

    const edges = timberEdges.map(timberEdge => {
        return {
            id: timberEdge.id,
            source: timberEdge.source,
            sourceHandle: timberEdge.resource,
            target: timberEdge.target,
            targetHandle: timberEdge.resource
        }
    });

    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
        nodes,
        edges,
        "LR"
    )

    console.log(nodes, edges);

    return <ReactFlow
        nodes={layoutedNodes}
        edges={layoutedEdges}
        fitView
        nodeTypes={nodeTypes}
    >
        <Controls />
        <Background color="#aaa" gap={16} />
    </ReactFlow>
}