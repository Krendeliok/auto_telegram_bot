import axios from "axios";

export default class ProducersService {
    static async getAll() {
        const response = await axios.get("/api/v1/producers");
        return response
    }
}