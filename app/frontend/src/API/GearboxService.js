import axios from "axios";

export default class GearboxService {
    static async getAll() {
        const response = await axios.get("/api/v1/gearboxes");
        return response
    }
}