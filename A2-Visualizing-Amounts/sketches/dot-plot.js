const dotPlot = (p) => {
    let table;
    let ageGroups = {};
    
    p.preload = () => {
        table = p.loadTable('data/daily_usage.csv', 'csv', 'header');
    };
    
    p.setup = () => {
        let canvas = p.createCanvas(800, 400);
        canvas.parent('dot-plot-container');
        p.noLoop();
        processData();
    };
    
    function processData() {
        for (let i = 0; i < table.getRowCount(); i++) {
            let ageGroup = table.getString(i, 'age_group');
            if (!ageGroups[ageGroup]) {
                ageGroups[ageGroup] = [];
            }
            let workStudyHours = table.getNum(i, 'work_or_study_hours');
            ageGroups[ageGroup].push(workStudyHours);
        }
        
        for (let group in ageGroups) {
            let sum = ageGroups[group].reduce((a, b) => a + b, 0);
            ageGroups[group] = sum / ageGroups[group].length;
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
        let dotSpacing = chartWidth / groups.length;
        
        drawYAxis(margin, chartHeight, maxValue);
        
        for (let i = 0; i < groups.length; i++) {
            let x = margin.left + (i * dotSpacing) + (dotSpacing / 2);
            let y = p.map(values[i], 0, maxValue, p.height - margin.bottom, margin.top);
            
            p.stroke(150);
            p.strokeWeight(1);
            p.line(x, p.height - margin.bottom, x, y);
            
            p.fill(255, 100, 100);
            p.stroke(200, 50, 50);
            p.strokeWeight(3);
            p.ellipse(x, y, 15, 15);
            
            p.fill(0);
            p.noStroke();
            p.textAlign(p.CENTER);
            p.textSize(12);
            p.text(values[i].toFixed(1), x, y - 20);
            
            p.push();
            p.translate(x, p.height - margin.bottom + 15);
            p.rotate(-0.3);
            p.text(groups[i], 0, 0);
            p.pop();
        }
        
        let minValue = Math.min(...values);
        let minIndex = values.indexOf(minValue);
        let minX = margin.left + (minIndex * dotSpacing) + (dotSpacing / 2);
        let minY = p.map(minValue, 0, maxValue, p.height - margin.bottom, margin.top);
        
        drawAnnotation(minX + 60, minY + 50, 'Lowest work/\nstudy hours', minX, minY + 8);
        
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
        p.text('Average Work/Study Hours', 0, 0);
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
            let value = ((maxValue / numTicks) * i).toFixed(1);
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
        p.stroke(0, 150, 200);
        p.strokeWeight(2);
        p.fill(0, 150, 200);
        
        p.line(textX, textY - 15, arrowToX, arrowToY);
        
        let angle = p.atan2(arrowToY - (textY - 15), arrowToX - textX);
        p.push();
        p.translate(arrowToX, arrowToY);
        p.rotate(angle);
        p.triangle(-8, -4, -8, 4, 0, 0);
        p.pop();
        
        p.fill(230, 245, 255);
        p.stroke(0, 150, 200);
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

new p5(dotPlot);