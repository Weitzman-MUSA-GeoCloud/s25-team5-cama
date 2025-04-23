const margin = { top: 20, right: 50, bottom: 40, left: 50 };
const width = Math.min(650, window.innerWidth * 0.35) - margin.left - margin.right;
const height = Math.min(450, window.innerHeight * 0.50) - margin.top - margin.bottom;
let svg;

const columnMap = {
  'White increasingly diverse (23)': ['Black1', 'White2', 'Hispanic2'],
  'White/Black increasingly Hispanic (17)': ['Black2', 'White2', 'Hispanic2'],
  'Hispanic strong holds (13)': ['Black1', 'White1', 'Hispanic1'],
  'Majority minority track (5)': ['Black2', 'White1', 'Hispanic2'],
  'White & Hispanic (4)': ['Black1', 'White2', 'Hispanic1'],
  'Majority minority (3)': ['Black2', 'White1', 'Hispanic1'],
  'Outlier (1)': ['Black1', 'White1', 'Hispanic2'],
};

const categoryColors = {
  'White increasingly diverse (23)': 'rgba(120, 160, 133, 0.8)', // #78a085
  'White/Black increasingly Hispanic (17)': 'rgba(207, 120, 99, 0.8)', // #cf7863
  'Hispanic strong holds (13)': 'rgba(152, 143, 197, 0.8)', // #988FC5
  'Majority minority track (5)': 'rgba(225, 163, 179, 0.8)', // #E1A3B3
  'White & Hispanic (4)': 'rgba(153, 207, 171, 0.8)', // #99CFAB
  'Majority minority (3)': 'rgba(247, 197, 72, 0.8)', // #F7C548
  'Outlier (1)': 'rgba(165, 146, 123, 0.8)', // #A5927B
};


const colorMap = {
  'Black1': '#cf7863',
  'Black2': '#cf7863',
  'White1': '#78a085',
  'White2': '#78a085',
  'Hispanic1': '#988FC5',
  'Hispanic2': '#988FC5',
};

async function lineChart(lineEL, data, selectedGroup = 'Hispanic strong holds (13)') {
  let selectedColumns = columnMap[selectedGroup] || columnMap['Hispanic strong holds (13)'];

  // Ensure data is formatted correctly
  data.forEach((d) => {
    d.Year = +d.Year;
    selectedColumns.forEach((col) => {
      d[col] = +d[col];
    });
  });

  // Append dropdown menu to the line chart container
  const select = d3.select('#select-button');
  select.selectAll('option').remove();

  select.selectAll('option')
    .data(Object.keys(columnMap))
    .enter().append('option')
    .text((d) => d)
    .attr('value', (d) => d);

  svg = lineEL
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const x = d3.scaleLinear()
    .domain(d3.extent(data, (d) => d.Year))
    .range([0, width]);

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, (d) => d3.max(selectedColumns, (col) => d[col]))])
    .range([height, 0]);

  // Fixed colors based on the category
  const color = (col) => colorMap[col] || 'gray';

  // Add X axis
  svg.append('g')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format('d')))
    .style('font-family', 'Lato, sans-serif')
    .style('font-size', '11px');

  // Add Y axis
  const yAxis = svg.append('g')
    .attr('class', 'y-axis')
    .call(d3.axisLeft(y))
    .style('font-family', 'Lato, sans-serif')
    .style('font-size', '11px');

  // Line group container
  const lineGroup = svg.append('g');

  function update(selectedGroup) {
    // Update the selected columns based on the new selection
    selectedColumns = columnMap[selectedGroup];

    const newYDomain = [0, d3.max(data, (d) => d3.max(selectedColumns, (col) => d[col]))];
    y.domain(newYDomain);

    // Transition the Y axis
    yAxis.transition()
      .duration(1000)
      .call(d3.axisLeft(y));

    // Transition the Y axis
    svg.selectAll('.y-axis')
      .transition()
      .duration(1000)
      .call(d3.axisLeft(y));

    // Bind new data to the existing lines
    const lines = lineGroup.selectAll('path')
      .data(selectedColumns);

    // Exit phase: remove any lines that are no longer relevant
    lines.exit()
      .transition()
      .duration(500)
      .style('opacity', 0)
      .remove();

    // Enter phase: add any new lines that are being added
    const linesEnter = lines.enter().append('path')
      .attr('fill', 'none')
      .attr('stroke', (d) => color(d))
      .attr('stroke-width', 5)
      .style('opacity', 0);

    // Update phase: update existing lines and transition them smoothly to new data
    linesEnter.merge(lines)
      .transition()
      .duration(1000)
      .style('opacity', 1)
      .attr('d', (d) => {
        return d3.line()
          .x((dataPoint) => x(dataPoint.Year))
          .y((dataPoint) => y(dataPoint[d]))(data);
      });
  }


  // Initial chart rendering
  update(selectedGroup);

  // Set default selection
  const defaultGroup = 'White increasingly diverse (23)';

  d3.select('#select-button')
    .style('background-color', categoryColors[defaultGroup])
    .style('transition', 'background-color 0.3s ease-in-out'); // Smooth transition

  // Dropdown event listener
  d3.select('#select-button').on('change', (event) => {
    const newSelectedGroup = d3.select(event.target).property('value');

    // Call the update function for the line chart
    update(newSelectedGroup);

    // Update the dropdown background color with transparency
    const selectedColor = categoryColors[newSelectedGroup] || 'rgba(255, 255, 255, 0.5)'; // Default to semi-transparent white
    d3.select('#select-button')
      .style('background-color', selectedColor)
      .style('transition', 'background-color 0.3s ease-in-out'); // Smooth transition
  });

  // Create a set of unique labels and colors
  const uniqueLegendItems = Array.from(
    new Map(Object.entries(colorMap).map(([key, value]) => [value, key])).values(),
  );

  const legend = svg.append('g')
    .attr('transform', `translate(${width - 50}, 10)`); // Adjust position

  uniqueLegendItems.forEach((key, index) => {
    const legendRow = legend.append('g')
      .attr('transform', `translate(0, ${index * 20})`); // Space out legend items

    legendRow.append('rect')
      .attr('width', 12)
      .attr('height', 12)
      .attr('fill', colorMap[key]); // Use filtered color map

    legendRow.append('text')
      .attr('x', 18)
      .attr('y', 10)
      .style('font-size', '12px')
      .style('font-family', 'Lato, sans-serif')
      .text(key.replace(/\d/, '')); // Remove numbers from labels
  });
}

export { lineChart };