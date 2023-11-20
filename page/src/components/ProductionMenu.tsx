import { useContext } from "react"
import { TimberbornContext } from "../pyodideContext";


export function ProductionMenu() {
    const timberborn = useContext(TimberbornContext);
    const factions = timberborn.getFactions();

    return <div>
        Faction:
        <select>
            {factions.map(
                factionName => {return <option value={factionName}>{factionName}</option>}
            )}
        </select>
    </div>
}