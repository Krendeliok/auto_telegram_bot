import axios from "axios";

export default class FeedbackService {
    static async create({name, phone, advertisement_id = 0}) {
        let data = {
            name: name,
            phone: phone,
        }
        if (advertisement_id !== 0) {
            data.advertisement_id = advertisement_id
        }
        const response = await axios.post("/feedbacks", data);
        return response
    }
}