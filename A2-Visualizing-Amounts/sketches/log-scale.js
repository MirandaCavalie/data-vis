const logScale = (p) => {
    let table;
    let ageGroups = {};
    
    p.preload = () => {
        table = p.loadTable('data/daily_usage.csv', 'csv', 'header');
    };
    
    p.setup = () => {
        let canvas = p.createCanvas(800, 400);
        canvas.parent('log-scale-container');
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
        
        let margin = { left: 80, right: 40, top: 50, bottom: 80 };
        let chartWidth = p.width - margin.left - margin.right;
        let chartHeight = p.height - margin.top - margin.bottom;
        let maxValue = Math.max(...values);
        let barWidth = chartWidth / groups.length;
        
        for (let i = 0; i < groups.length; i++) {
            let x = margin.left + (i * barWidth);
            
            let logValue = Math.log10(values[i]);
            let logMax = Math.log10(maxValue);
            
            let barHeight = p.map(logValue, 0, logMax, 0, chartHeight);
            let y = margin.top + chartHeight - barHeight;
            
            p.fill(150, 100, 255);
            p.stroke(100, 50, 200);
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
        
        p.stroke(0);
        p.strokeWeight(2);
        p.line(margin.left, margin.top, margin.left, p.height - margin.bottom);
        p.line(margin.left, p.height - margin.bottom, p.width - margin.right, p.height - margin.bottom);
        
        p.fill(0);
        p.noStroke();
        p.textAlign(p.RIGHT, p.CENTER);
        p.textSize(11);
        
        let logTicks = [10, 100, 1000];
        for (let tickValue of logTicks) {
            if (tickValue <= maxValue) {
                let logTick = Math.log10(tickValue);
                let logMaxVal = Math.log10(maxValue);
                let y = p.map(logTick, 0, logMaxVal, p.height - margin.bottom, margin.top);
                
                p.stroke(0);
                p.line(margin.left - 5, y, margin.left, y);
                
                p.noStroke();
                p.text(tickValue, margin.left - 10, y);
            }
        }
        
        p.fill(0);
        p.textSize(16);
        p.textAlign(p.CENTER);
        
        p.push();
        p.translate(15, p.height/2);
        p.rotate(-p.HALF_PI);
        p.textSize(12);
        p.text('Number of Users (log scale)', 0, 0);
        p.pop();
        
        p.textSize(12);
        p.fill(0);
        p.text('Age Group', p.width/2, p.height - 25);
        
        p.textSize(10);
        p.fill(100);
        p.text('Y-axis: logarithmic scale (10, 100, 1000...)', p.width/2, p.height - 10);
    };
};

new p5(logScale);