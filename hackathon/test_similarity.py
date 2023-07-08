from room_assignment import fill_up_rooms 


def test_similarity_ones():

    available_space_in_room = [2,5,4,1]
    posters_in_room = [
    [0,1,2,3], #13
    [4,5], #14
    [6,7,8,9,10,12], #11
    [15]
    ]

    A = np.zeros((16,16))
    A[10,11] = 1
    A[11,12] = 1
    A[4,14] = 1
    A[3,13] = 1


    posters_in_room, available_space_in_room = fill_up_rooms(available_space_in_room, posters_in_room, A)
    
    if (posters_in_room == [1, 4, 3, 1])==True:
        return True
    if (available_space_in_room[0] == [0, 1, 2, 3, 13]) == True:
        return True
