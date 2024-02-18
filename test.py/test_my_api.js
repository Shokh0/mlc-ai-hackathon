const axios = require('axios');

async function testAssistResponse() {
    const url = 'http://127.0.0.1:8000/api/assistAnswer/';

    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };

    const data = {
        'assist_api': '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',
        'voice_api': 'ada49528-f84e-4a78-b9fe-46184041184e:a84a029d-9169-4956-9652-6dc476f612ce',
        'assistant_id': 'asst_3Gt1cdlU7BzTwYmMqJ48erHx',
        'text_for_request': 'Menga kompaniya haqida gapirib bering?',
    };

    try {
        const response = await axios.post(url, data, { headers });
        console.log(response.data.assist_response);
    } catch (error) {
        console.error(error.message);
    }
}

async function testWebCrawler() {
    const url = 'http://127.0.0.1:8000/api/getWebCrawler/';

    const headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    };

    const data = {
        'full_url': 'https://ztour.uz/'
    };

    try {
        const response = await axios.post(url, data, { headers });
        console.log(response.data.status);
    } catch (error) {
        console.error(error.message);
    }
}


// testAssistResponse()

// testWebCrawler();
