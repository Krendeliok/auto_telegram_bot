import axios from "axios";

export default class FuelService {
    static async getAll() {
        const response = await axios.get("/fuels");
        return response
    }
}