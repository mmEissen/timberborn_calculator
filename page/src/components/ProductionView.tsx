import { useContext } from "react"
import { Graphviz } from 'graphviz-react';
import { TimberbornContext } from "../pyodideContext";


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

    const dot = timberborn.dotGraph(params.faction, params.product)

    return <Graphviz dot={dot}></Graphviz>
}