import { useContext } from "react"
import { TimberbornContext } from "../pyodideContext";


interface Params {
    product: string | null;
    onProductChanged: (v: string | null) => any;
    faction: string | null;
    onFactionChanged: (v: string | null) => any;
    amount: number;
    onAmountChanged: (v: number) => any;
}

export function ProductionMenu(params: Params) {
    const timberborn = useContext(TimberbornContext);

    const factions = timberborn.getFactions();
    const products = params.faction != null ? timberborn.getProducts(params.faction) : [];

    return <div>
        <div>
            Faction:
            <select 
                value={params.faction != null ? params.faction : "__null"}
                onChange={e => params.onFactionChanged(e.target.value === "__null" ? null : e.target.value)}
            >
                <option key={null} value={"__null"}>Select a faction</option>
                {factions.map(
                    factionName => {return <option key={factionName} value={factionName}>{factionName}</option>}
                )}
            </select>
        </div>
        <div>
            Product:
            <select
                value={params.product != null ? params.product : "__null"}
                onChange={e => params.onProductChanged(e.target.value === "__null" ? null : e.target.value)}
                disabled={params.faction === null}
            >
                <option key={null} value={"__null"}>Select a product</option>
                {products.map(
                    productName => {return <option key={productName} value={productName}>{productName}</option>}
                )}
            </select>
        </div>
        <div>
            Amount:
            <input type="number" value={params.amount} onChange={e => params.onAmountChanged(+e.target.value)} />
        </div>
    </div>
}