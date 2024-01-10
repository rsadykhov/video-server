import pandas as pd
from videos import models



def get_recommendations(video_pk: int):
    video_pk = int(video_pk)
    try:
        # Extracting categories data
        categories_df = pd.DataFrame(models.VideoCategoriesThrough.objects.all().values())[["video_id", "category_id"]]
        categories_df = pd.get_dummies(categories_df, columns=["category_id"], drop_first=True).groupby(by="video_id").sum()
        # Extracting tags data
        tags_df = pd.DataFrame(models.VideoTagsThrough.objects.all().values())[["video_id", "tag_id"]]
        tags_df = pd.get_dummies(tags_df, columns=["tag_id"], drop_first=True).groupby(by="video_id").sum()
    except KeyError:
        return {"similar":[], "opposite":[]}
    # Correlation between features in db
    df = categories_df.merge(tags_df, how="outer", left_index=True, right_index=True)
    df = df.T.corr()
    try:
        corr_s = df[video_pk].drop(video_pk, axis=0).dropna().sort_values(ascending=True)
        opposite = []
        for i in range(3):
            try:
                opposite.append(int(corr_s.index[i]))
            except IndexError:
                break
        corr_s.sort_values(ascending=False)
        similar = []
        for i in range(3):
            try:
                similar.append(int(corr_s.index[i]))
            except IndexError:
                break
        return {"similar":similar, "opposite":opposite}
    except KeyError:
        return {"similar":[], "opposite":[]}