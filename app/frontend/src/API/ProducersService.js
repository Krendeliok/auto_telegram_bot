import axios from "axios";

export default class ProducersService {
    static async getAll() {
        const response = await axios.get("/producers");
        return response
    }
}