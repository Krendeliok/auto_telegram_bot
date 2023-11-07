import axios from "axios";

export default class AdvertisementService {
    static async getAll(filter, limit = 3, page = 1) {
        const response = await axios.get("/advertisements", {
            params: {
                _limit: limit,
                _page: page,
                ...filter.asDict()
            }
        });
        return response
    }

    static async getMaxPrice() {
        const response = await axios.get("/advertisements/get_max_price");
        return response;
    }
}