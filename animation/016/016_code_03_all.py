        # default value of 'gamma' is '0 DEGREE'.

        self.move_camera(theta=-135 * DEGREES, run_time=2)
        self.move_camera(phi=45 * DEGREES, run_time=2)
        self.move_camera(phi=0, run_time=2)
        self.move_camera(theta=-90 * DEGREES, run_time=2)
        self.move_camera(gamma=0, run_time=1)
        self.move_camera(gamma=45 * DEGREES, run_time=2)
        self.move_camera(gamma=-45 * DEGREES, run_time=2)
