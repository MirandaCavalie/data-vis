const interactive = (p) => {
    let table;
    let ageGroups = {};
    let hoveredBar = -1;
    
    p.preload = () => {
        table = p.loadTable('data/daily_usage.csv', 'csv', 'header');
    };
    
    p.setup = () => {
        let canvas = p.createCanvas(800, 400);
        canvas.parent('interactive-container');
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
    
    function checkHover() {
        let groups = Object.keys(ageGroups);
        let margin = { left: 80, right: 40, top: 50, bottom: 70 };
        let chartWidth = p.width - margin.left - margin.right;
        let barWidth = chartWidth / groups.length;
        
        if (p.mouseX >= margin.left && p.mouseX <= p.width - margin.right &&
            p.mouseY >= margin.top && p.mouseY <= p.height - margin.bottom) {
            let relativeX = p.mouseX - margin.left;
            hoveredBar = Math.floor(relativeX / barWidth);
            if (hoveredBar < 0 || hoveredBar >= groups.length) {
                hoveredBar = -1;
            }
        } else {
            hoveredBar = -1;
        }
    }
    
    p.draw = () => {
        p.background(255);
        checkHover();
        
        let groups = Object.keys(ageGroups);
        let values = Object.values(ageGroups);
        
        let margin = { left: 80, right: 40, top: 50, bottom: 70 };
        let chartWidth = p.width - margin.left - margin.right;
        let chartHeight = p.height - margin.top - margin.bottom;
        let maxValue = Math.max(...values);
        let barWidth = chartWidth / groups.length;
        
        for (let i = 0; i < groups.length; i++) {
            let x = margin.left + (i * barWidth);
            let barHeight = p.map(values[i], 0, maxValue, 0, chartHeight);
            let y = margin.top + chartHeight - barHeight;
            
            if (i === hoveredBar) {
                p.fill(255, 150, 0);
                p.stroke(200, 100, 0);
                p.strokeWeight(3);
            } else {
                p.fill(100, 150, 255);
                p.stroke(50, 100, 200);
                p.strokeWeight(2);
            }
            
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
        
        p.stroke(0);
        p.strokeWeight(2);
        p.line(margin.left, margin.top, margin.left, p.height - margin.bottom);
        p.line(margin.left, p.height - margin.bottom, p.width - margin.right, p.height - margin.bottom);
        
        p.fill(0);
        p.noStroke();
        p.textSize(14);
        p.textAlign(p.CENTER);
        
        p.push();
        p.translate(15, p.height/2);
        p.rotate(-p.HALF_PI);
        p.textSize(12);
        p.text('Number of Users', 0, 0);
        p.pop();
        
        p.textSize(12);
        p.text('Age Group', p.width/2, p.height - 10);
        
        if (hoveredBar >= 0) {
            let total = values.reduce((a, b) => a + b, 0);
            let percentage = ((values[hoveredBar] / total) * 100).toFixed(1);
            
            let tooltipX = p.mouseX;
            let tooltipY = p.mouseY - 50;
            
            if (tooltipX > p.width - 100) tooltipX = p.width - 100;
            if (tooltipX < 100) tooltipX = 100;
            
            p.fill(255, 255, 220);
            p.stroke(100);
            p.strokeWeight(2);
            p.rectMode(p.CENTER);
            p.rect(tooltipX, tooltipY, 120, 45, 5);
            
            p.fill(0);
            p.noStroke();
            p.textAlign(p.CENTER, p.CENTER);
            p.textSize(11);
            p.text(groups[hoveredBar], tooltipX, tooltipY - 12);
            p.text('Users: ' + values[hoveredBar], tooltipX, tooltipY + 3);
            p.text(percentage + '%', tooltipX, tooltipY + 16);
            
            p.rectMode(p.CORNER);
        }
    };
};

new p5(interactive);