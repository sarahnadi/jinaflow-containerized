from jina import Flow

flow = (
    Flow(port=8080, protocol='http')  # Use HTTP for communication
    .add(name='encoder', uses='jinaai+docker://TransformerTorchEncoder/latest', install_requirements=True)
    .add(
        uses='jinaai+docker://AnnLiteIndexer/latest',
        install_requirements=True,
        uses_with={
            'columns': [('supplier', 'str'), ('price', 'float'), ('attr_t_product_type', 'str'), ('attr_t_product_colour', 'str')],
            'n_dim': 768,
        },
    )
)
flow.to_docker_compose_yaml('docker-compose.yml')