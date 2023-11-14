import axios from "axios";

export default class FuelService {
    static async getAll() {
        const response = await axios.get("/api/v1/fuels");
        return response
    }
}