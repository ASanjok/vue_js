const fs = require('fs');
const csv = require('csv-parser');
const axios = require('axios');

// path to file CSV
const csvFilePath = 'D:/skudra_server_test_planeadsbdata_20241204.csv';

// delay function 
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
let d = 0;

// post request function
async function sendPostRequest(data) {
    try {
        const response = await axios.post('http://localhost:3000/sendMessage', data);
        console.log('Message sent successfully:\n---'+d);
        d++;
    } catch (error) {
        console.error('Error sending message:', error);
    }
}



const stream = fs.createReadStream(csvFilePath).pipe(csv());

stream.on('data', async (row) => {
    // Pause the stream to enforce delay
    stream.pause();

    try {
        // Parse the first value of the row as JSON
        const message = JSON.parse(Object.values(row)[0]);

        // Send POST request
        await sendPostRequest(message);
    } catch (err) {
        console.error('Error parsing JSON:', err, 'for row:', row);
    }

    // Wait for 100 milliseconds before resuming the stream
    await delay(100);
    stream.resume();
});

stream.on('end', () => {
    console.log('CSV file processing finished.');
});


// // Чтение и обработка файла CSV
// fs.createReadStream(csvFilePath)
//     .pipe(csv())
//     .on('data', async (row) => {
//         // Если строка уже содержит JSON, напрямую ее парсим
//         try {
//             const message = JSON.parse(Object.values(row)[0]);  

//             // Отправляем данные в виде POST запроса
//             await sendPostRequest(message);
            
//             // Задержка 100 мс между запросами
//             await delay(1000000);
//         } catch (err) {
//             console.error('Error parsing JSON:', err, 'for row:', row);
//             return 0
//         }
//     })
//     .on('end', () => {
//         console.log('CSV file processing finished.');
//     });
