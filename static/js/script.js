function createChart(canvasId, data, label) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const existingChart = Chart.getChart(canvasId);
    if (existingChart) {
        existingChart.destroy();
    }

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['0', '1', '2', '3'], // Ось X
            datasets: [{
                label: label,
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                lineTension: 0.1,
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: true,
            scales: {
                y: { beginAtZero: true,
                     max: 100,
                     }
            }
        }
    });
}

function updateCharts() {
    fetch('/SCS/get_server_data/')
        .then(response => response.text())
        .then(text => {
            console.log("Ответ от сервера:", text);
            return JSON.parse(text);
        })
        .then(data => {
            if (!data) {
                console.error("Ошибка: пустой JSON!");
                return;
            }

            if (typeof data !== "object") {
                console.error("Ошибка: некорректный формат JSON!", data);
                return;
            }

            console.log("JSON-данные:", data);

            document.querySelectorAll('.server-canvas').forEach((canvas, index) => {
                const serverId = canvas.dataset.serverId;

                if (!data[`server_${serverId}`]) {
                    console.warn(`Данных для server_${serverId} нет в JSON!`);
                    return;
                }

                const serverData = data[`server_${serverId}`];

                const newCpuData = serverData.cpuLoad?.[0] === 'Ошибка' ? null : serverData.cpuLoad?.[0] ?? 0;
                const newMemoryData = serverData.memoryLoad?.[0] === 'Ошибка' ? null : serverData.memoryLoad?.[0] ?? 0;
                const newDiskData = serverData.diskLoad?.[0] === 'Ошибка' ? null : serverData.diskLoad?.[0] ?? 0;
                const newInternetData = serverData.internetSpeed?.[0] === 'Ошибка' ? null : serverData.internetSpeed?.[0] ?? 0;

                console.log(`Обновляем сервер ${serverId}: CPU=${newCpuData}, RAM=${newMemoryData}`);

                const cpuCanvas = Chart.getChart(`cpuLoadCanvas${serverId}`);
                const memoryCanvas = Chart.getChart(`memoryLoadCanvas${serverId}`);
                const diskCanvas = Chart.getChart(`diskLoadCanvas${serverId}`);
                const internetCanvas = Chart.getChart(`internetSpeedCanvas${serverId}`);

                const maxDataPoints = 10;

                if (cpuCanvas) {
                    if (cpuCanvas.data.datasets[0].data.length >= maxDataPoints) {
                        cpuCanvas.data.datasets[0].data.shift(); // Убираем старые данные
                        cpuCanvas.data.labels.shift(); // Убираем старую метку времени
                    }
                    cpuCanvas.data.datasets[0].data.push(newCpuData);
                    cpuCanvas.data.labels.push(new Date().toLocaleTimeString()); // Добавляем метку времени
                    cpuCanvas.update();
                }

                if (memoryCanvas) {
                    if (memoryCanvas.data.datasets[0].data.length >= maxDataPoints) {
                        memoryCanvas.data.datasets[0].data.shift();
                        memoryCanvas.data.labels.shift();
                    }
                    memoryCanvas.data.datasets[0].data.push(newMemoryData);
                    memoryCanvas.data.labels.push(new Date().toLocaleTimeString());
                    memoryCanvas.update();
                }

                if (diskCanvas) {
                    if (diskCanvas.data.datasets[0].data.length >= maxDataPoints) {
                        diskCanvas.data.datasets[0].data.shift();
                        diskCanvas.data.labels.shift();
                    }
                    diskCanvas.data.datasets[0].data.push(newDiskData);
                    diskCanvas.data.labels.push(new Date().toLocaleTimeString());
                    diskCanvas.update();
                }

                if (internetCanvas) {
                    if (internetCanvas.data.datasets[0].data.length >= maxDataPoints) {
                        internetCanvas.data.datasets[0].data.shift();
                        internetCanvas.data.labels.shift();
                    }
                    internetCanvas.data.datasets[0].data.push(newInternetData);
                    internetCanvas.data.labels.push(new Date().toLocaleTimeString());
                    internetCanvas.update();
                }
            });

        })
        .catch(error => console.error("Ошибка при обновлении данных:", error));
}

function initCharts() {
    console.log('Инициализация графиков...');

    document.querySelectorAll('.server-canvas').forEach((canvas) => {
        const serverId = canvas.dataset.serverId;

        createChart(`cpuLoadCanvas${serverId}`, [], 'CPU Load');
        createChart(`memoryLoadCanvas${serverId}`, [], 'Memory Load');
        createChart(`diskLoadCanvas${serverId}`, [], 'Disk Load');
        createChart(`internetSpeedCanvas${serverId}`, [], 'Internet Speed');
    });
}
initCharts();
setInterval(updateCharts, 5000);
