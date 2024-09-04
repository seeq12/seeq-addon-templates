import * as d3 from 'd3';
import * as _ from 'lodash';

/**
 * A simple d3 pie chart
 */
class Chart {
  radius: number;
  svg: any;

  constructor(private id: string) {
  }

  render(width: number, height: number, data: [{ name: string, value: number, valueUnitOfMeasure: string }]) {
    const margin = 20;
    this.radius = Math.min(width, height) / 2 - margin;

    d3.selectAll(`#${this.id} > *`).remove();

    this.svg = d3.select(`#${this.id}`)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // Compute the position of each group on the pie:
    var pie = d3.pie()
      .value(d => _.get(d, 'value'));

    // shape helper to build arcs:
    var arcGenerator = d3.arc()
      .innerRadius(0)
      .outerRadius(this.radius);

    var data_ready = pie(data);

    // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
    this.svg
      .selectAll('mySlices')
      .data(data_ready)
      .enter()
      .append('path')
      .attr('d', arcGenerator)
      .attr('fill', d => _.get(d, 'data.color'))
      .attr("stroke", "black")
      .style("stroke-width", "2px")
      .style("opacity", 0.7);

    // Now add the annotation. Use the centroid method to get the best coordinates
    this.svg
      .selectAll('mySlices')
      .data(data_ready)
      .enter()
      .append('text')
      .text(d => _.get(d, 'data.name'))
      .attr("transform", d => "translate(" + arcGenerator.centroid(d) + ")")
      .style("text-anchor", "middle")
      .style("font-size", 14);

    this.svg
      .selectAll('mySlices')
      .data(data_ready)
      .enter()
      .append('text')
      .text(d => Math.round(+_.get(d, 'data.value')) + ' ' + _.get(d, 'data.valueUnitOfMeasure'))
      .attr("transform", d => "translate(" + arcGenerator.centroid(d)[0] + ',' + (arcGenerator.centroid(d)[1] + 15) + ")")
      .style("text-anchor", "middle")
      .style("font-size", 14);
  }
}

export default Chart;