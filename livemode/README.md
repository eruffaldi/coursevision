

#Example

lastimg = data.get("img")
if lastimg is None:
  lastimg = cv2.imread("../example.jpg",cv2.IMREAD_COLOR)
  data["img"] = lastimg
nextimg = lastimg*2

imshow(nextimg)
cv2.resizeWindow("live",640,400)

#Ideas
- HTML5 widgets (trackbar...)
- Python live video and repeat execution for every frame