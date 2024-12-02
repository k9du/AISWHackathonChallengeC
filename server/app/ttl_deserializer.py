from rdflib import Graph, Namespace

DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCT = Namespace("http://purl.org/dc/terms/")


def deserialize(file, i):
    g = Graph()
    g.parse(file, format="turtle")

    for dataset in g.subjects(predicate=DCT.title, object=None):
        title = g.value(subject=dataset, predicate=DCT.title)
        creator = g.value(subject=dataset, predicate=DCT.creator)
        subject = g.value(subject=dataset, predicate=DCT.subject)
        description = g.value(subject=dataset, predicate=DCT.description)
        publisher = g.value(subject=dataset, predicate=DCT.publisher)
        contributor = g.value(subject=dataset, predicate=DCT.contributor)
        date = g.value(subject=dataset, predicate=DCT.date)
        data_type = g.value(subject=dataset, predicate=DCT.type)
        format = g.value(subject=dataset, predicate=DCT.format)
        id = g.value(subject=dataset, predicate=DCT.identifier)
        source = g.value(subject=dataset, predicate=DCT.source)
        language = g.value(subject=dataset, predicate=DCT.language)
        relation = g.value(subject=dataset, predicate=DCT.relation)
        rights = g.value(subject=dataset, predicate=DCT.rights)

    sections = {
        "db_id": i,
        "title": title,
        "creator": creator,
        "subject": subject,
        "description": description,
        "publisher": publisher,
        "contributor": contributor,
        "date": date,
        "data_type": data_type,
        "format": format,
        "id": id,
        "source": source,
        "language": language,
        "relation": relation,
        "rights": rights
    }
    return sections
