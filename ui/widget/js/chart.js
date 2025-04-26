function createChart(data, containerId) {
    const container = d3.select(`#${containerId}`);
    container.select("svg").remove();

    const width = container.node().clientWidth;;
    const height = container.node().clientHeight;
    const margin = { top: 20, right: 20, bottom: 50, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.year))
        .range([0, innerWidth]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .range([innerHeight, 0]);

    // Split actual and projected data
    const actualData = data.filter(d => !d.projected);
    const projectedData = data.slice(-2); // last two points (e.g., 2024 and 2025)

    // Draw solid line for actual data
    svg.append("path")
        .datum(actualData)
        .attr("fill", "none")
        .attr("stroke", "#0f4d90")
        .attr("stroke-width", 2)
        .attr("d", d3.line()
            .x(d => x(d.year))
            .y(d => y(d.value))
        );

    // Draw dotted line for projection (2024 -> 2025)
    if (projectedData.length === 2) {
        svg.append("path")
            .datum(projectedData)
            .attr("fill", "none")
            .attr("stroke", "#f99300")
            .attr("stroke-width", 2)
            .attr("stroke-dasharray", "4 4") // dotted line
            .attr("d", d3.line()
                .x(d => x(d.year))
                .y(d => y(d.value))
            );
    }

    // Circles for actual data
    svg.selectAll("circle.actual")
        .data(actualData)
        .enter().append("circle")
        .attr("class", "actual")
        .attr("cx", d => x(d.year))
        .attr("cy", d => y(d.value))
        .attr("r", 3)
        .attr("fill", "#0f4d90");

    // Circle for projected point
    svg.selectAll("circle.projected")
        .data(data.filter(d => d.projected))
        .enter().append("circle")
        .attr("class", "projected")
        .attr("cx", d => x(d.year))
        .attr("cy", d => y(d.value))
        .attr("r", 4)
        .attr("fill", "#f99300");

    // X-axis
    svg.append("g")
        .attr("transform", `translate(0,${innerHeight})`)
        .call(d3.axisBottom(x).tickFormat(d3.format("d")));

    // Y-axis
    const yTicks = d3.range(0, d3.max(data, d => d.value), 50000);

    // Y-axis
    svg.append("g")
        .call(d3.axisLeft(y)
        .tickValues(yTicks)
        .tickFormat(d => {
            // Format the tick value and append 'k' for thousands
            return d >= 1000 ? `${d / 1000}k` : d;
        })
    );

    // X-axis label
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("x", innerWidth / 2)
        .attr("y", innerHeight + 35)
        .text("Year")
        .style("font-size", "12px");

    // Y-axis label
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .attr("x", -innerHeight / 2)
        .attr("y", -40)
        .text("Market Value")
        .style("font-size", "12px");
}

export { createChart }