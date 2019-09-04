from adminapp import db, User, Post

db.create_all()

admin = User("BrettMZig", "apr231616")
db.session.add(admin)


post1 = Post("My First Post",
             "Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
             sed do eiusmod tempor incididunt ut labore et dolore magna \
             aliqua. Netus et malesuada fames ac turpis egestas maecenas \
             pharetra convallis. Ac orci phasellus egestas tellus rutrum. \
             Mi tempus imperdiet nulla malesuada pellentesque elit eget. \
             Aliquet enim tortor at auctor. Ipsum consequat nisl vel pretium \
             lectus. Dignissim diam quis enim lobortis scelerisque fermentum.")
db.session.add(post1)


post2 = Post("My Second Post",
             "Sed odio morbi quis commodo odio aenean sed. Nisl purus in \
             mollis nunc sed id. Et magnis dis parturient montes nascetur \
             ridiculus mus. Mi ipsum faucibus vitae aliquet nec. \
             \
             Feugiat nibh sed pulvinar proin gravida hendrerit. Ultricies \
             integer quis auctor elit. Venenatis a condimentum vitae sapien \
             pellentesque habitant morbi tristique. Ante metus dictum at \
             tempor commodo ullamcorper a lacus vestibulum. Facilisi morbi \
             tempus iaculis urna id volutpat lacus laoreet.")
db.session.add(post2)

db.session.commit()
