from typing import Dict, Any
import json

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.memories import (
    CollectionsOutput,
    CollectionPointsDestroyOutput,
    MemoryRecallOutput,
    MemoryPointOutput,
    MemoryPointDeleteOutput,
    MemoryPointsDeleteByMetadataOutput,
    MemoryPointsOutput,
)
from grinning_cat_python_sdk.models.api.nested.memories import CollectionsItem
from grinning_cat_python_sdk.models.dtos import Why, MemoryPoint, FilterSource


class MemoryEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/memory"

    # Memory Collections API

    def get_memory_collections(self, agent_id: str) -> CollectionsOutput:
        """
        This endpoint returns the collections of memory points.
        :param agent_id: The agent ID.
        :return: CollectionsOutput, a list of collections of memory points.
        """
        return self.get(
            self.format_url("/collections"),
            agent_id,
            output_class=CollectionsOutput,
        )

    def delete_all_memory_collection_points(self, agent_id: str) -> CollectionPointsDestroyOutput:
        """
        This endpoint deletes all memory points in all collections for the agent identified by the agentId parameter.
        :param agent_id: The agent ID.
        :return: CollectionPointsDestroyOutput, a message indicating the number of memory points deleted.
        """
        return self.delete(
            self.format_url("/collections"),
            agent_id,
            output_class=CollectionPointsDestroyOutput,
        )

    def delete_all_single_memory_collection_points(
        self, collection: str, agent_id: str
    ) -> CollectionPointsDestroyOutput:
        """
        This method deletes all the points in a single collection of memory.
        :param collection: The collection to delete.
        :param agent_id: The agent ID.
        :return: CollectionPointsDestroyOutput, a message indicating the number of memory points deleted.
        """
        return self.delete(
            self.format_url(f"/collections/{collection}"),
            agent_id,
            output_class=CollectionPointsDestroyOutput,
        )

    def post_memory_collections(self, collection_id: str, agent_id: str) -> CollectionsItem:
        """
        This endpoint returns the collections of memory points.
        :param collection_id: The ID of the collection to create.
        :param agent_id: The agent ID.
        :return: CollectionsItem, the collection created.
        """
        return self.post_json(
            self.format_url(f"/collections/{collection_id}"),
            agent_id,
            output_class=CollectionsItem,
        )

    # END Memory Collections API

    # Memory Points API

    def get_memory_recall(
        self,
        text: str,
        agent_id: str,
        user_id: str,
        k: int | None = None,
        metadata: Dict[str, Any] | None = None,
        chat_id: str | None = None,
    ) -> MemoryRecallOutput:
        """
        This endpoint retrieves memory points based on the input text. The text parameter is the input text for which
        the memory points are retrieved. The k parameter is the number of memory points to retrieve.
        :param text: The input text for which the memory points are retrieved.
        :param agent_id: The agent ID.
        :param user_id: The user ID to filter the memory points.
        :param k: The number of memory points to retrieve.
        :param metadata: The metadata to filter the memory points.
        :param chat_id: The chat id, optional
        :return: MemoryRecallOutput, a list of memory points retrieved.
        """
        query = {"text": text}
        if k:
            query["k"] = k  # type: ignore
        if metadata:
            query["metadata"] = json.dumps(metadata)  # type: ignore

        return self.get(
            self.format_url("/recall"),
            agent_id,
            output_class=MemoryRecallOutput,
            user_id=user_id,
            query=query,
            chat_id=chat_id,
        )

    def post_memory_point(
        self,
        collection: str,
        agent_id: str,
        user_id: str,
        memory_point: MemoryPoint,
    ) -> MemoryPointOutput:
        """
        This method posts a memory point.
        :param collection: The collection to post the memory point.
        :param agent_id: The agent ID.
        :param user_id: The user ID to associate with the memory point.
        :param memory_point: The memory point to post.
        :return: MemoryPointOutput, the memory point posted.
        """
        if user_id and not memory_point.metadata.get("source"):
            metadata = memory_point.metadata
            metadata["source"] = user_id
            memory_point.metadata = metadata

        return self.post_json(
            self.format_url(f"/collections/{collection}/points"),
            agent_id,
            output_class=MemoryPointOutput,
            payload=memory_point.model_dump(),
        )

    def put_memory_point(
        self,
        collection: str,
        agent_id: str,
        user_id: str,
        memory_point: MemoryPoint,
        point_id: str,
    ) -> MemoryPointOutput:
        """
        This method puts a memory point, for the agent identified by the agent_id parameter.
        :param collection: The collection to put the memory point.
        :param agent_id: The agent ID.
        :param user_id: The user ID to associate with the memory point.
        :param memory_point: The memory point to put.
        :param point_id: The ID of the memory point to put.
        :return: MemoryPointOutput, the memory point put.
        """
        if user_id and not memory_point.metadata.get("source"):
            metadata = memory_point.metadata
            metadata["source"] = user_id
            memory_point.metadata = metadata

        return self.put(
            self.format_url(f"/collections/{collection}/points/{point_id}"),
            agent_id,
            output_class=MemoryPointOutput,
            payload=memory_point.model_dump(),
        )

    def delete_memory_point(
        self,
        collection: str,
        agent_id: str,
        point_id: str,
    ) -> MemoryPointDeleteOutput:
        """
        This endpoint deletes a memory point.
        :param collection: The collection to delete the memory point.
        :param agent_id: The agent ID.
        :param point_id: The ID of the memory point to delete.
        :return: MemoryPointDeleteOutput, a message indicating the memory point deleted.
        """
        return self.delete(
            self.format_url(f"/collections/{collection}/points/{point_id}"),
            agent_id,
            output_class=MemoryPointDeleteOutput,
        )

    def delete_memory_points_by_metadata(
        self,
        collection: str,
        agent_id: str,
        metadata: Dict[str, Any] | None = None,
    ) -> MemoryPointsDeleteByMetadataOutput:
        """
        This endpoint deletes memory points based on the metadata. The metadata parameter is a dictionary of key-value
        pairs that the memory points must match.
        :param collection: The collection to delete the memory points.
        :param agent_id: The agent ID.
        :param metadata: The metadata to filter the memory points.
        :return: MemoryPointsDeleteByMetadataOutput, a message indicating the number of memory points deleted.
        """
        return self.delete(
            self.format_url(f"/collections/{collection}/points"),
            agent_id,
            output_class=MemoryPointsDeleteByMetadataOutput,
            payload=metadata,
        )

    def get_memory_points(
        self,
        collection: str,
        agent_id: str,
        limit: int | None = None,
        offset: int | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> MemoryPointsOutput:
        """
        This endpoint retrieves memory points. The limit parameter is the maximum number of memory points to retrieve.
        The offset parameter is the number of memory points to skip.
        :param collection: The collection to retrieve the memory points.
        :param agent_id: The agent ID.
        :param limit: The maximum number of memory points to retrieve.
        :param offset: The number of memory points to skip.
        :param metadata: The metadata to filter the memory points.
        :return: MemoryPointsOutput, a list of memory points retrieved.
        """
        query = {}
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        if metadata:
            query["metadata"] = json.dumps(metadata)  # type: ignore

        return self.get(
            self.format_url(f"/collections/{collection}/points"),
            agent_id,
            output_class=MemoryPointsOutput,
            query=query,
        )

    def has_source(self, agent_id: str, filter_source: FilterSource, chat_id: str | None = None) -> bool:
        """
        Checks if the given filter source exists for a specified agent.

        This method determines whether a specific source, defined by the given filter_source, is associated with the
        provided agent in the memory database.
        It optionally considers a specific chat ID when filtering the data. The result indicates the existence of such a
        source.

        Args:
            agent_id: Unique identifier of the agent for which the check is performed.
            filter_source: FilterSource object that defines the source or hash to check.
            chat_id: An optional chat identifier to narrow the scope of the check. If not provided, the check will
                operate in a broader context.

        Returns:
            A boolean value indicating whether the specified filter source exists in the agent's memory database.
        """
        metadata = {"source": filter_source.source} if filter_source.source else {"hash": filter_source.hash}
        if chat_id:
            metadata["chat_id"] = chat_id

        collection_name = "declarative" if chat_id is None else "episodic"
        points = self.get_memory_points(collection_name, agent_id, metadata=metadata)

        return len(points.points) > 0

    # END Memory Points API
