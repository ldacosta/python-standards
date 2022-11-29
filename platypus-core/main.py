"""Platypus-core main methods."""
import json
import logging
from argparse import ArgumentParser
from pathlib import Path

import pyarrow as pa
import structlog
from igraph_mims import read_arrow_graph_from_feather, write_arrow_graph_to_feather
from structlog import configure, make_filtering_bound_logger
from structlog.stdlib import get_logger

logger = get_logger()


def json_dumps(text: str, *args, **kwargs):
    """Allows UTF-8 encoding in the json dumps function, i.e. 8.8µs is not 8.8\u00b5s."""
    return json.dumps(text, ensure_ascii=False, *args, **kwargs)


def run(graph_path: Path, output_path: Path, log_level: str):
    """Platypus-core entrypoint."""
    # Set the global log level
    log_level = logging.getLevelName(log_level)
    configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(sort_keys=True, serializer=json_dumps),
        ],
        wrapper_class=make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )

    output_path.mkdir(exist_ok=True)

    graph = read_arrow_graph_from_feather(file_path=graph_path)
    graph_attrs = graph.graph_attrs.to_pandas()
    logger.info(f"Read graph {graph_attrs['name'][0]}")

    # Change the graph name
    graph_attrs["name"] = ["test"]
    graph.graph_attrs = pa.Table.from_pandas(graph_attrs)
    write_arrow_graph_to_feather(graph, output_path)
    logger.info(
        f"Graph saved to output path: {output_path} with name {graph.graph_attrs['name'][0]}"
    )


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Main entrypoint for the Omic-Correlation-Clustering process"
    )
    parser.add_argument(
        "-i", "--input-path", type=Path, help="The graph file input path", required=True
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=Path,
        help="The graph file output path",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--log-level",
        type=str.upper,
        help="The log level used to output log messages",
        default="INFO",
        choices=["ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"],
    )
    args = parser.parse_args()
    run(
        graph_path=args.input_path,
        output_path=args.output_path,
        log_level=args.log_level,
    )
