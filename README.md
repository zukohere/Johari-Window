# Johari-Window
Johari Window App

Deployed at https://self-awareness-app.herokuapp.com/.
(Pet project under continuous development)

Uses modified flask/mongoDB username/password scheme inspired by https://github.com/PrettyPrinted/mongodb-user-login and Johari Window concept inspired by https://www.fearlessculture.design/blog-posts/the-johari-window to build self-awareness within a community, friend group, family, work environment, or other team structure. In short, it helps a person understand what of their qualities they are putting "out there" effectively.

A user will select from a list of adjectives to describe themselves, and then ask other members of their team to fill out say same form about the original user. Any adjective will fit into one of four categories.

- Arena. The user selects the adjective to describe themselves, and so do other members of the team.
- Facade. Though the user selects the adjective to describe themselves, other members of the team do not.
- Blindspot. Though the user does not select the adjective to describe themselves, other members of the team do.
- Unknown. Neither the user nor team members select the adjective to describe the user.

The data is visualized using a modified ordered lollipop method inspired by https://www.d3-graph-gallery.com/graph/lollipop_ordered.html.