function createChart(data, containerId) {
    // Select the graph container
    const container = d3.select(`#${containerId}`);

    // Remove any previous chart to avoid duplicates
    container.select("svg").remove();

    // Define dimensions
    const width = 350;
    const height = 185;
    const margin = { top: 20, right: 0, bottom: 40, left: 60 };

    // Select the container & append SVG
    const svg = container.append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // Set up x-scale (using lower_bound as labels)
    const x = d3.scaleBand()
        .domain(data.map(d => `${d.lower_bound} - ${d.upper_bound}`)) // Format range labels
        .range([0, width - margin.left - margin.right])
        .padding(0.2);

    // Set up y-scale
    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.property_count)])
        .range([height - margin.top - margin.bottom, 0]);

    // Draw bars
    svg.selectAll("rect")
        .data(data)
        .enter().append("rect")
        .attr("x", d => x(`${d.lower_bound} - ${d.upper_bound}`))
        .attr("y", d => y(d.property_count))
        .attr("width", x.bandwidth())
        .attr("height", d => height - margin.bottom - margin.top - y(d.property_count))
        .attr("fill", "steelblue");

    // Add x-axis
    svg.append("g")
        .attr("transform", `translate(0,${height - margin.top - margin.bottom})`)
        .call(d3.axisBottom(x).tickFormat(label => {
            const parts = label.split(' - ');
            const formatted = parts.map(val => d3.format(".2s")(+val));  // convert to number & format
            return `${formatted[0]} - ${formatted[1]}`;
        }))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-0.5em")
        .attr("dy", "0.5em")
        .attr("transform", "rotate(-45)");

    // Add y-axis
    svg.append("g")
    .call(d3.axisLeft(y).tickFormat(d3.format(".0s")));

    // X-axis label
    svg.append("text")
    .attr("text-anchor", "middle")
    .attr("x", (width - margin.left - margin.right) / 2)
    .attr("y", height - margin.bottom + 50)
    .text("Property Assessment Value")
    .style("font-size", "12px");

    // Y-axis label
    svg.append("text")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .attr("x", -height + 120)
    .attr("y", -margin.left + 12)
    .text("Number of properties")
    .style("font-size", "12px");
}

export { createChart };