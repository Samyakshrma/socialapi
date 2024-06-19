
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {Id} not found")