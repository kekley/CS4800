import axios from 'axios';

export default () => {

    return axios.create({
        baseURL: `https://smalltalk.kekley.online`,
        headers: {
            "Accept": "application/json",
        }
    });

}
