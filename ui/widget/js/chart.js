function createChart(data, containerId) {
    const container = d3.select(`#${containerId}`);
    container.select("svg").remove();

    const width = 350;
    const height = 185;
    const margin = { top: 20, right: 0, bottom: 40, left: 60 };

    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // Scales
    const x = d3.scaleLinear()
        .domain(d3.extent(data, d => d.year))
        .range([0, width - margin.left - margin.right]);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .range([height - margin.top - margin.bottom, 0]);

    // Line generator
    const line = d3.line()
        .x(d => x(d.year))
        .y(d => y(d.value));

    // Draw line
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2)
        .attr("d", line);

    // Draw circles
    svg.selectAll("circle")
        .data(data)
        .enter().append("circle")
        .attr("cx", d => x(d.year))
        .attr("cy", d => y(d.value))
        .attr("r", 3)
        .attr("fill", "steelblue");

    // X-axis
    svg.append("g")
        .attr("transform", `translate(0,${height - margin.top - margin.bottom})`)
        .call(d3.axisBottom(x).tickFormat(d3.format("d")));

    // Y-axis
    svg.append("g")
        .call(d3.axisLeft(y).tickFormat(d3.format(".0s")));

    // X-axis label
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("x", (width - margin.left - margin.right) / 2)
        .attr("y", height - margin.bottom + 30)
        .text("Year")
        .style("font-size", "12px");

    // Y-axis label
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2 + 20)
        .attr("y", -margin.left + 12)
        .text("Market Value ($)")
        .style("font-size", "12px");
}

export { createChart }