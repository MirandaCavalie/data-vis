const heatmap = (p) => {
    let table;
    let ageGroups = ['13-18', '19-25', '26-35', '36-45', '46-60', '60+'];
    let months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'];
    let heatmapData = [];
    
    p.preload = () => {
        table = p.loadTable('data/daily_usage.csv', 'csv', 'header');
    };
    
    p.setup = () => {
        let canvas = p.createCanvas(900, 400);
        canvas.parent('heatmap-container');
        p.noLoop();
        processData();
    };
    
    function processData() {
        let dataByAgeAndMonth = {};
        
        for (let ageGroup of ageGroups) {
            dataByAgeAndMonth[ageGroup] = {};
            for (let month of months) {
                dataByAgeAndMonth[ageGroup][month] = [];
            }
        }
        
        for (let i = 0; i < table.getRowCount(); i++) {
            let ageGroup = table.getString(i, 'age_group');
            let dateStr = table.getString(i, 'date');
            let screenTime = table.getNum(i, 'total_screen_time');
            
            let monthNum = parseInt(dateStr.split('-')[1]);
            let monthNames = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            let month = monthNames[monthNum];
            
            if (months.includes(month)) {
                dataByAgeAndMonth[ageGroup][month].push(screenTime);
            }
        }
        
        for (let i = 0; i < ageGroups.length; i++) {
            heatmapData[i] = [];
            for (let j = 0; j < months.length; j++) {
                let values = dataByAgeAndMonth[ageGroups[i]][months[j]];
                if (values.length > 0) {
                    let sum = values.reduce((a, b) => a + b, 0);
                    heatmapData[i][j] = sum / values.length;
                } else {
                    heatmapData[i][j] = 0;
                }
            }
        }
    }
    
    function getColor(value, minVal, maxVal) {
        let normalized = p.map(value, minVal, maxVal, 0, 1);
        let r = normalized * 255;
        let b = (1 - normalized) * 255;
        return p.color(r, 100, b);
    }
    
    p.draw = () => {
        p.background(255);
        
        let margin = { left: 80, right: 40, top: 50, bottom: 50 };
        let chartWidth = p.width - margin.left - margin.right;
        let chartHeight = p.height - margin.top - margin.bottom;
        
        let cellWidth = chartWidth / months.length;
        let cellHeight = chartHeight / ageGroups.length;
        
        let allValues = heatmapData.flat();
        let minVal = Math.min(...allValues.filter(v => v > 0));
        let maxVal = Math.max(...allValues);
        
        for (let i = 0; i < ageGroups.length; i++) {
            for (let j = 0; j < months.length; j++) {
                let value = heatmapData[i][j];
                let x = margin.left + (j * cellWidth);
                let y = margin.top + (i * cellHeight);
                
                if (value > 0) {
                    p.fill(getColor(value, minVal, maxVal));
                } else {
                    p.fill(220);
                }
                
                p.stroke(255);
                p.strokeWeight(2);
                p.rect(x, y, cellWidth, cellHeight);
                
                if (value > 0) {
                    p.fill(0);
                    p.noStroke();
                    p.textAlign(p.CENTER, p.CENTER);
                    p.textSize(9);
                    p.text(value.toFixed(1), x + cellWidth/2, y + cellHeight/2);
                }
            }
        }
        
        let maxI = 0, maxJ = 0;
        for (let i = 0; i < ageGroups.length; i++) {
            for (let j = 0; j < months.length; j++) {
                if (heatmapData[i][j] === maxVal) {
                    maxI = i;
                    maxJ = j;
                }
            }
        }
        let maxCellX = margin.left + (maxJ * cellWidth) + cellWidth/2;
        let maxCellY = margin.top + (maxI * cellHeight) + cellHeight/2;
        
        p.noFill();
        p.stroke(255, 200, 0);
        p.strokeWeight(4);
        p.rect(margin.left + (maxJ * cellWidth), margin.top + (maxI * cellHeight), cellWidth, cellHeight);
        
        drawAnnotation(maxCellX + 80, maxCellY - 20, 'Peak screen\ntime', maxCellX + cellWidth/2, maxCellY);
        
        p.fill(0);
        p.noStroke();
        p.textSize(11);
        
        p.textAlign(p.RIGHT, p.CENTER);
        for (let i = 0; i < ageGroups.length; i++) {
            let y = margin.top + (i * cellHeight) + (cellHeight / 2);
            p.text(ageGroups[i], margin.left - 10, y);
        }
        
        p.textAlign(p.CENTER, p.TOP);
        for (let j = 0; j < months.length; j++) {
            let x = margin.left + (j * cellWidth) + (cellWidth / 2);
            p.text(months[j], x, p.height - margin.bottom + 10);
        }
        
        p.textSize(14);
        p.textAlign(p.CENTER);
    };
    
    function drawAnnotation(textX, textY, label, arrowToX, arrowToY) {
        p.stroke(255, 150, 0);
        p.strokeWeight(2);
        p.fill(255, 150, 0);
        
        p.line(textX, textY + 15, arrowToX, arrowToY);
        
        let angle = p.atan2(arrowToY - (textY + 15), arrowToX - textX);
        p.push();
        p.translate(arrowToX, arrowToY);
        p.rotate(angle);
        p.triangle(-8, -4, -8, 4, 0, 0);
        p.pop();
        
        p.fill(255, 250, 220);
        p.stroke(255, 150, 0);
        p.strokeWeight(2);
        p.rectMode(p.CENTER);
        p.rect(textX, textY, 85, 30, 5);
        
        p.fill(0);
        p.noStroke();
        p.textAlign(p.CENTER, p.CENTER);
        p.textSize(10);
        p.text(label, textX, textY);
        p.rectMode(p.CORNER);
    }
};

new p5(heatmap);