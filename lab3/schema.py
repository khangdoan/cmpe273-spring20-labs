from ariadne import gql, load_schema_from_path

schema = gql(
    """
    type Student{
        id: ID!
        name: String!
    }
    type Class{
        name: String!
        students: [Student!]!
    }
    """
)