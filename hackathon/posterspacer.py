"""Contains the PosterSpacer class to optimally space posters in a given
room.
"""


import numpy as np


class PosterSpacer:
    """Provide room parameters to optimally space posters."""

    def __init__(
        self,
        room_lower_left_corner_position: tuple,
        room_length: int | float,
        room_width: int | float,
    ):
        """PosterSpacer can be used to determine the row anchors for the
        poster wall rows, the poster wall rows themselves and count the
        number of posters for a given room.

        Args:
            room_lower_left_corner_position (tuple): Coordinates of the room's lower left corner.
            room_length (int | float): Length of the room.
            room_width (int | float): Width of the room.

        Raises:
            ValueError: If room_length is not a positive number.
            ValueError: If room width is not a positive number.
            ValueError: If dimension of room_lower_left_corner_position is not equal to 2.
        """
        self._room_length = (
            room_length if room_length >= room_width else room_width
        )
        if self.room_length <= 0:
            raise ValueError(
                "room_length must be positive, got"
                f" {self.room_length} instead."
            )
        self._room_width = (
            room_width if room_width < room_length else room_length
        )
        if self.room_width <= 0:
            raise ValueError(
                f"room_width must be positive, got {self.room_width} instead."
            )
        self._room_lower_left_corner_position = room_lower_left_corner_position
        if not len(self.room_lower_left_corner_position) == 2:
            raise ValueError(
                "Dimensions of room_lower_left_corner_position has to be 2,"
                f" got {len(self._room_lower_left_corner_position)} instead."
            )
        self._padding = 0.25
        self._padded_poster_length = 2 * self._padding + 1
        self._length_linspace = None
        self._width_linspace = None

    @property
    def room_length(self):
        return self._room_length

    @room_length.setter
    def room_length(self, room_length: int | float):
        if room_length <= 0:
            raise ValueError(
                f"room_length must be positive, got {room_length} instead."
            )
        self._room_length = room_length

    @room_length.deleter
    def room_length(self):
        raise PermissionError("Deleting room_length is forbidden!")

    @property
    def room_width(self):
        return self._room_width

    @room_width.setter
    def room_width(self, room_width: int | float):
        if room_width <= 0:
            raise ValueError(
                f"room_width must be positive, got {room_width} instead."
            )
        self._room_width = room_width

    @room_width.deleter
    def room_width(self):
        raise PermissionError("Deleting room_width is forbidden!")

    @property
    def room_lower_left_corner_position(self):
        return self._room_lower_left_corner_position

    @room_lower_left_corner_position.setter
    def room_lower_left_corner_position(
        self, room_lower_left_corner_position: tuple
    ):
        if not len(room_lower_left_corner_position) == 2:
            raise ValueError(
                "Dimensions of room_lower_left_corner_position has to be 2,"
                f" got {len(room_lower_left_corner_position)} instead."
            )
        self._room_lower_left_corner_position = room_lower_left_corner_position

    @room_lower_left_corner_position.deleter
    def room_lower_left_corner_position(self):
        raise PermissionError(
            "Deleting room_lower_left_corner_position is forbidden!"
        )

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, padding: int | float):
        if padding < 0:
            raise ValueError(
                f"padding cannot be negative, got {padding} instead."
            )
        self._padding = padding

    @padding.deleter
    def padding(self):
        raise PermissionError("Deleting padding is forbidden!")

    @property
    def padded_poster_length(self):
        return self._padded_poster_length

    @padded_poster_length.setter
    def padded_poster_length(self):
        raise PermissionError("Setting padded_poster_length is forbidden!")

    @padded_poster_length.deleter
    def padded_poster_length(self):
        raise PermissionError("Deleting padded_poster_length is forbidden!")

    @property
    def length_linspace(self):
        return self._length_linspace

    @length_linspace.setter
    def length_linspace(self):
        raise PermissionError("Setting length_linspace is forbidden!")

    @length_linspace.deleter
    def length_linspace(self):
        raise PermissionError("Deleting length_linspace is forbidden!")

    @property
    def width_linspace(self):
        return self._width_linspace

    @width_linspace.setter
    def width_linspace(self):
        raise PermissionError("Setting width_linspace is forbidden!")

    @width_linspace.deleter
    def width_linspace(self):
        raise PermissionError("Deleting width_linspace is forbidden!")

    def _create_rows(self):
        """Calculate number of theoretical rows of poster walls based on
        the size of the room.
        """
        number_of_posters_along_room_length = (
            self.room_length // (2 * self.padded_poster_length) + 1
        )
        number_of_posters_along_room_width = (
            self.room_width // self.padded_poster_length - 1
        )
        self._length_linspace = np.linspace(
            self.room_lower_left_corner_position[0],
            (number_of_posters_along_room_length - 1)
            * 2
            * self.padded_poster_length
            + self.room_lower_left_corner_position[0],
            int(number_of_posters_along_room_length),
        )
        self._width_linspace = np.linspace(
            self.room_lower_left_corner_position[1]
            + 0.5
            + 0.5 * self.padded_poster_length,
            self.room_lower_left_corner_position[1]
            + self.room_width
            - 0.5
            - 0.5 * self.padded_poster_length,
            int(number_of_posters_along_room_width),
        )

    def get_row_anchor_nodes(self) -> dict[list[tuple]]:
        """Calculate and return the nodes that anchor the various poster
        rows as a dictionary of the bottom and top row of anchor nodes
        with the nodes being a tuple of its coordinates.

        Returns:
            dict[list[tuple]]: Bottom and top rows of nodes anchoring the various poster rows.
        """
        self._create_rows()
        dict_of_row_anchor_nodes = {}
        bottom_row_anchor_nodes = []
        top_row_anchor_nodes = []
        for length_position in self.length_linspace:
            new_tuple = (
                length_position,
                (
                    self.width_linspace[0]
                    + self.room_lower_left_corner_position[1]
                )
                / 2,
            )
            bottom_row_anchor_nodes.append(new_tuple)
            new_tuple = (
                length_position,
                (
                    self.width_linspace[-1]
                    + self.room_lower_left_corner_position[1]
                    + self.room_width
                )
                / 2,
            )
            top_row_anchor_nodes.append(new_tuple)
        dict_of_row_anchor_nodes["bottom_row_anchor_nodes"] = (
            bottom_row_anchor_nodes
        )
        dict_of_row_anchor_nodes["top_row_anchor_nodes"] = top_row_anchor_nodes
        return dict_of_row_anchor_nodes

    def get_poster_row_nodes(self) -> dict[dict[list[tuple]]]:
        """Calculate and return the poster positions as tuples of
        coordinates as lists of poster wall rows sorted into a
        dictionary of left and right (back and front) poster wall rows,
        which are again sorted in a dictionary by row index.

        Returns:
            dict[dict[list[tuple]]]: Poster rows sorted by poster walls and row indices.
        """
        self._create_rows()
        dict_of_poster_row_nodes = {}
        for index, length_position in enumerate(self.length_linspace):
            dict_of_poster_row_nodes[index] = {}
            dict_of_poster_row_nodes[index]["left_poster_row_nodes"] = []
            if index == 0:
                dict_of_poster_row_nodes[index].pop("left_poster_row_nodes")
            dict_of_poster_row_nodes[index]["right_poster_row_nodes"] = []
            if (
                index == len(self.length_linspace) - 1
                and self.room_lower_left_corner_position[0]
                + self.room_length
                - length_position
                < self.padded_poster_length
            ):
                dict_of_poster_row_nodes[index].pop("right_poster_row_nodes")
            for width_position in self.width_linspace:
                try:
                    dict_of_poster_row_nodes[index][
                        "left_poster_row_nodes"
                    ].append(
                        (
                            length_position - self.padded_poster_length / 2,
                            width_position,
                        )
                    )
                except:
                    pass
                try:
                    dict_of_poster_row_nodes[index][
                        "right_poster_row_nodes"
                    ].append(
                        (
                            length_position + self.padded_poster_length / 2,
                            width_position,
                        )
                    )
                except:
                    pass
        return dict_of_poster_row_nodes

    @classmethod
    def get_number_of_posters():
        ...


if __name__ == "__main__":
    ps = PosterSpacer((7, 68), 10, 6)
    ran = ps.get_row_anchor_nodes()
    print(ran)
    prn = ps.get_poster_row_nodes()
    print(prn)
