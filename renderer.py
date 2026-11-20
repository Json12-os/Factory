import moderngl
import moderngl_window as mglw
import numpy as np


playerX =0
playerY =0
windowSizewidth = 800
windowSizeheight = 600
tilesize = 50
s = []
color = []
gridsize = []
for i in range(2*windowSizewidth//tilesize):
    gridsize.append([])
    for b in range(2*windowSizeheight//tilesize):
        x0 = (i*tilesize+2)/windowSizewidth-1
        y0  = (b*tilesize+2)/windowSizeheight-1
        x1  = ((i+1)*tilesize-2)/windowSizewidth-1
        y1  = ((b+1)*tilesize-2)/windowSizeheight-1
        gridsize[i].append({


            "surky":[
                x0, y0,
                x0, y1,
                x1, y1,

                x0, y0,
                x1, y1,
                x1, y0




            ],
            "colour": [0.0, 0.0, 1.0]
        })
        s.extend(gridsize[i][b]["surky"])
        color.extend(gridsize[i][b]["colour"] *6)




class App(mglw.WindowConfig):

    gl_version = (3, 3)
    title = "My First ModernGL Program"
    window_size = (windowSizewidth, windowSizeheight)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ctx = self.wnd.ctx

        # Vertex data
        vertices = np.array(
        #[
        #    -1.0, -1.0,
        #     -1.0, 1.0,
        #     1.0,  1.0,
        #
        #    -1.0, -1.0,
        #    1.0, -1.0,
        #    1.0,  1.0,
        #],
        s,
          dtype="f4")
        colors = np.array(color, dtype="f4")

        self.color_vbo = self.ctx.buffer(colors.tobytes())

        # Vertex shader
        vertex_shader = """
        #version 330

        in vec2 in_position;
        in vec3 in_color;

        out vec3 vertex_color;

        void main() {
        gl_Position = vec4(in_position, 0.0, 1.0);
        vertex_color = in_color;
        }
        """
        
        
        old = """
        #version 330

        in vec2 in_position;

        void main() {
            gl_Position = vec4(in_position, 0.0, 1.0);
        }
        """

        # Fragment shader
        fragment_shader = """
        #version 330

        in vec3 vertex_color;

        out vec4 fragColor;

        void main() {
        fragColor = vec4(vertex_color, 1.0);
        }

        """
        old = """
        #version 330

        out vec4 fragColor;

        void main() {
            vec2 pixel =gl_FragCoord.xy;

            fragColor = vec4(
            pixel.x/800.0,
            pixel.y/600.0,
            1.0,
            1.0);
        }
        """

        # Compile shaders
        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )

        # Create GPU buffer
        self.vbo = self.ctx.buffer(vertices.tobytes())

        # Create vertex array
        old ="""
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, "2f", "in_position")]
        )"""

        self.vao = self.ctx.vertex_array(
    self.program,
    [
        (self.vbo, "2f", "in_position"),
        (self.color_vbo, "3f", "in_color")
    ]
)

    def on_render(self, time, frame_time):
        self.ctx.clear(0.1, 0.1, 0.1)

        self.vao.render(moderngl.TRIANGLES)


App.run()