let port;

let last_record;

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * Connects to the serial port.
 */
function connect() {
    if (port) {
        console.log(port + ' disconnected.');
        port.disconnect();
        $("#connect").html('連接裝置');
        port = null;
    }
    else {
        serial.requestPort().then(selectedPort => {
            port = selectedPort;
            port.connect().then(() => {
                console.log(port + ' connected.');
                $("#connect").html('取消連接');
                port.onReceive = data => {
                    let textDecoder = new TextDecoder();
                    // alert(textDecoder.decode(data));
                    alert("已完成錄製脈像");
                    // FILEPATH: /Users/jason/Coding/DTCM/static/js/device_handler.js
                    $("#last_record").html("上次錄製：" + formatDate(new Date()));

                    axios.post("/api/upload", {
                        room: room,
                        data: textDecoder.decode(data)
                    }).then(response => {
                        console.log(response.data);
                    }).catch(error => {
                        console.error('Error:', error);
                        alert("上傳失敗");
                    });
                }

                port.onReceiveError = error => {
                    console.error('Receive error: ' + error);
                    alert("傳輸發生錯誤，請嘗試重新連接裝置或聯繫管理員");
                };
            }, error => {
                console.error('Connection error: ' + error);
                alert("連接發生錯誤，請嘗試重新連接裝置或聯繫管理員");
            });
        }).catch(error => {
            console.error('Connection error: ' + error);
            alert("連接發生錯誤，請嘗試重新連接裝置或聯繫管理員");
        });
    }
}

function connect_doctor() {
    if (port) {
        console.log(port + ' disconnected.');
        port.disconnect();
        $("#connect").html('連接裝置');
        port = null;
    }
    else {
        serial.requestPort().then(selectedPort => {
            port = selectedPort;
            port.connect().then(() => {
                console.log(port + ' connected.');
                $("#connect").html('取消連接');
                port.onReceive = data => {
                    let textDecoder = new TextDecoder();
                    // alert(textDecoder.decode(data));
                    alert("已完成錄製脈像");
                    // FILEPATH: /Users/jason/Coding/DTCM/static/js/device_handler.js
                    $("#last_record").html("上次錄製：" + formatDate(new Date()));

                    axios.post("/api/upload", {
                        room: room,
                        data: textDecoder.decode(data)
                    }).then(response => {
                        console.log(response.data);
                    }).catch(error => {
                        console.error('Error:', error);
                        alert("上傳失敗");
                    });
                }

                port.onReceiveError = error => {
                    console.error('Receive error: ' + error);
                    alert("傳輸發生錯誤，請嘗試重新連接裝置或聯繫管理員");
                };
            }, error => {
                console.error('Connection error: ' + error);
                alert("連接發生錯誤，請嘗試重新連接裝置或聯繫管理員");
            });
        }).catch(error => {
            console.error('Connection error: ' + error);
            alert("連接發生錯誤，請嘗試重新連接裝置或聯繫管理員");
        });
    }
}

function record() {
    if (port) {
        port.send(new TextEncoder().encode('s')).then(() => {
            alert("已開始錄製脈像，請靜候一分鐘");
        })
            .catch(error => {
                console.error('Send error: ' + error);
                alert("傳輸發生錯誤，請嘗試重新連接裝置或聯繫管理員");
            });
    }
    else {
        alert('請先連接裝置');
    }
}

let pulse;

function load_pulse() {
    axios.get(`/api/get_pulse?room=${room}`).then(res => {
        $("#last_upload").html("病患上次上傳：" + res.data.date);
        $("#pulse_list").html(`
        <div class="card">
            <div class="card-body">
                <h6 class="text-muted card-subtitle mb-2">2024/2/13 16:58:21</h6><button class="btn btn-primary" type="button" onclick="play();">播放</button>
            </div>
        </div>
        `)
        // $("#pulse").html(response.data);
        pulse = res.data.data;
    }).catch(error => {
        // console.error('Error:', error);
        alert("載入脈像發生錯誤，請嘗試重新載入或聯繫管理員");
    });
}

function play() {
    if(pulse){
        if(port){
            port.send(new TextEncoder().encode(pulse)).then(() => {
                alert("已開始播放脈像");
            })
            .catch(error => {
                console.error('Send error: ' + error);
                alert("傳輸發生錯誤，請嘗試重新連接裝置或聯繫管理員");
            });
        }
        else{
            alert("請先連接裝置");
        }
    }
    else{
        alert("請先載入脈像");
    }
}
