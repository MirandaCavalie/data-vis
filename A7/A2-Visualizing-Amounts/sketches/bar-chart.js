const barChart = (p) => {
    let table;
    let ageGroups = {};
    
    p.preload = () => {
        table = p.loadTable('data/daily_usage.csv', 'csv', 'header');
    };
    
    p.setup = () => {
        let canvas = p.createCanvas(800, 400);
        canvas.parent('bar-chart-container');
        p.noLoop();
        processData();
    };
    
    function processData() {
        for (let i = 0; i < table.getRowCount(); i++) {
            let ageGroup = table.getString(i, 'age_group');
            if (!ageGroups[ageGroup]) {
                ageGroups[ageGroup] = 0;
            }
            ageGroups[ageGroup]++;
        }
    }
    
    p.draw = () => {
        p.background(255);
        
        let groups = Object.keys(ageGroups);
        let values = Object.values(ageGroups);
        
        let margin = { left: 80, right: 40, top: 50, bottom: 70 };
        let chartWidth = p.width - margin.left - margin.right;
        let chartHeight = p.height - margin.top - margin.bottom;
        let maxValue = Math.max(...values);
        let barWidth = chartWidth / groups.length;
        
        drawYAxis(margin, chartHeight, maxValue);
        
        for (let i = 0; i < groups.length; i++) {
            let x = margin.left + (i * barWidth);
            let barHeight = p.map(values[i], 0, maxValue, 0, chartHeight);
            let y = margin.top + chartHeight - barHeight;
            
            p.fill(100, 150, 255);
            p.stroke(50, 100, 200);
            p.strokeWeight(2);
            p.rect(x + 10, y, barWidth - 20, barHeight);
            
            p.fill(0);
            p.noStroke();
            p.textAlign(p.CENTER);
            p.textSize(12);
            p.text(values[i], x + barWidth/2, y - 5);
            
            p.push();
            p.translate(x + barWidth/2, p.height - margin.bottom + 15);
            p.rotate(-0.3);
            p.text(groups[i], 0, 0);
            p.pop();
        }
        
        let maxIndex = values.indexOf(maxValue);
        let maxX = margin.left + (maxIndex * barWidth) + barWidth/2;
        let maxBarHeight = p.map(maxValue, 0, maxValue, 0, chartHeight);
        let maxY = margin.top + chartHeight - maxBarHeight;
        
        drawAnnotation(maxX, maxY - 40, 'Highest user\nconcentration', maxX, maxY - 10);
        
        p.stroke(0);
        p.strokeWeight(2);
        p.line(margin.left, margin.top, margin.left, p.height - margin.bottom);
        p.line(margin.left, p.height - margin.bottom, p.width - margin.right, p.height - margin.bottom);
        
        p.fill(0);
        p.noStroke();
        p.textSize(16);
        p.textAlign(p.CENTER);
        
        p.push();
        p.translate(15, p.height/2);
        p.rotate(-p.HALF_PI);
        p.textSize(12);
        p.text('Number of Users', 0, 0);
        p.pop();
        
        p.textSize(12);
        p.text('Age Group', p.width/2, p.height - 10);
    };
    
    function drawYAxis(margin, chartHeight, maxValue) {
        let numTicks = 5;
        
        p.fill(0);
        p.noStroke();
        p.textAlign(p.RIGHT, p.CENTER);
        p.textSize(11);
        
        for (let i = 0; i <= numTicks; i++) {
            let value = Math.round((maxValue / numTicks) * i);
            let y = p.map(i, 0, numTicks, p.height - margin.bottom, margin.top);
            
            p.stroke(0);
            p.strokeWeight(1);
            p.line(margin.left - 5, y, margin.left, y);
            
            if (i > 0) {
                p.stroke(220);
                p.strokeWeight(0.5);
                p.line(margin.left, y, p.width - margin.right, y);
            }
            
            p.noStroke();
            p.fill(0);
            p.text(value, margin.left - 10, y);
        }
    }
    
    function drawAnnotation(textX, textY, label, arrowToX, arrowToY) {
        p.stroke(255, 100, 0);
        p.strokeWeight(2);
        p.fill(255, 100, 0);
        
        p.line(textX, textY + 15, arrowToX, arrowToY);
        
        let angle = p.atan2(arrowToY - (textY + 15), arrowToX - textX);
        p.push();
        p.translate(arrowToX, arrowToY);
        p.rotate(angle);
        p.triangle(-8, -4, -8, 4, 0, 0);
        p.pop();
        
        p.fill(255, 250, 230);
        p.stroke(255, 100, 0);
        p.strokeWeight(2);
        p.rectMode(p.CENTER);
        p.rect(textX, textY, 100, 30, 5);
        
        p.fill(0);
        p.noStroke();
        p.textAlign(p.CENTER, p.CENTER);
        p.textSize(10);
        p.text(label, textX, textY);
        p.rectMode(p.CORNER);
    }
};

new p5(barChart);